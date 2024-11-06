"use client"
import React, { useEffect, useState, useCallback, useRef } from 'react'
import Webcam from 'react-webcam'
import Image from 'next/image'
import { Button } from "@/components/ui/button";
import { Mic, StopCircle } from 'lucide-react';
import { toast } from "sonner" 
import { chatSession } from "./../../../../../../utils/GeminiAIModal"
import { db } from '../../../../../../utils/db';
import { UserAnswer } from '../../../../../../utils/schema';
import { useUser } from '@clerk/nextjs';
import moment from 'moment';

const useSpeechRecognition = () => {
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const previousTranscriptRef = useRef('');

  const startListening = useCallback(() => {
    if ('webkitSpeechRecognition' in window) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }

      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event) => {
        const currentTranscript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        
        const newTranscript = currentTranscript.slice(previousTranscriptRef.current.length);
        setTranscript(prev => prev + newTranscript);
        previousTranscriptRef.current = currentTranscript;
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };

      previousTranscriptRef.current = '';
      recognitionRef.current.start();
      setIsListening(true);
    } else {
      toast.error('Speech recognition not supported in this browser');
    }
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  }, []);

  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  return { transcript, setTranscript, isListening, startListening, stopListening };
};

function RecordAnswerSection({ mockInterviewQuestion, activeQuestionIndex, interviewData }) {
  const [userAnswer, setUserAnswer] = useState('');
  const { transcript, setTranscript, isListening, startListening, stopListening } = useSpeechRecognition();
  const userAnswerRef = useRef('');
  const { user } = useUser();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setUserAnswer(transcript);
    userAnswerRef.current = transcript;
  }, [transcript]);

  const saveAnswer = async (finalAnswer) => {
    try {
      const feedbackPrompt = `Question: ${mockInterviewQuestion[activeQuestionIndex]?.question}, User Answer: ${finalAnswer} ,depends on questions and user answer for given interview question please give us rating for answer and feedback as area of improvement if any in just 3 to 5 lines to improve it in JSON format with rating field and feedback field`;

      const result = await chatSession.sendMessage(feedbackPrompt);
      const mockJsonResp = (result.response.text()).replace('```json', '').replace('```', '');
      const JsonFeedbackResp = JSON.parse(mockJsonResp);

      const resp = await db.insert(UserAnswer).values({
        mockIdRef: interviewData?.mockId,
        question: mockInterviewQuestion[activeQuestionIndex]?.question,
        correctAns: mockInterviewQuestion[activeQuestionIndex]?.answer,
        userAns: finalAnswer,
        feedback: JsonFeedbackResp?.feedback,
        rating: JsonFeedbackResp?.rating,
        userEmail: user?.primaryEmailAddress?.emailAddress,
        createdAt: moment().format('DD-MM-YYYY')
      });

      return resp;
    } catch (error) {
      console.error("Error saving answer:", error);
      throw error;
    }
  };

  const handleRecording = async () => {
    if (isListening) {
      stopListening();
      setLoading(true);

      try {
        const finalAnswer = userAnswerRef.current;
        
        if (finalAnswer.length < 10) {
          toast.error("Answer too short. Please record again.", { duration: 3000 });
          return;
        }

        const resp = await saveAnswer(finalAnswer);

        if (resp) {
          toast.success("Answer saved successfully", { duration: 3000 });
        }
      } catch (error) {
        toast.error("Failed to save answer. Please try again.", { duration: 3000 });
      } finally {
        setLoading(false);
        setTranscript('');
        setUserAnswer('');
      }
    } else {
      setUserAnswer('');
      startListening();
    }
  };

  return (
    <div className='flex items-center justify-center flex-col'>
      <div className='flex flex-col mt-20 justify-center items-center rounded-lg p-5'>
        <Image src='/webcam.png' width={200} height={200} className='absolute' alt="Webcam" />
        <Webcam
          mirrored={true}
          style={{
            height: 300,
            width: '100%',
            zIndex: 10,
          }}
        />
      </div>
      <Button 
        disabled={loading}
        variant="outline" 
        className="my-10"
        onClick={handleRecording}
      >
        {isListening ? (
          <h2 className='text-red-600 flex gap-2'>
            <StopCircle /> Stop Recording
          </h2>
        ) : (
          <h2 className='flex gap-2 text-primary items-center'>
            <Mic /> Record Answer
          </h2>
        )}
      </Button>
    </div>
  )
}

export default RecordAnswerSection