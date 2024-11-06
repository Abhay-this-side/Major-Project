"use client"
import React, { useEffect, useState } from 'react'
import { db } from '../../../../../utils/db';
import { MockInterview } from '../../../../../utils/schema';
import { eq } from 'drizzle-orm';
import { Button } from "@/components/ui/button";
import QuestionsSection from './_components/QuestionsSection'
import RecordAnswerSection from './_components/RecordAnswerSection'
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

function StartInterview({params}) {
    const router = useRouter();
    const [interviewData, setInterviewData] = useState();
    const [mockInterviewQuestion, setMockInterviewQuestion] = useState();
    const [activeQuestionIndex, setActiveQuestionIndex] = useState(0);
    const [isEnding, setIsEnding] = useState(false);

    useEffect(() => {
        GetInterviewDetails();
    }, []);

    const GetInterviewDetails = async () => {
        try {
            const result = await db.select().from(MockInterview)
                .where(eq(MockInterview.mockId, params.interviewId))

            if (result.length === 0) {
                toast.error("Interview not found");
                return;
            }

            const jsonMockResp = JSON.parse(result[0].jsonMockResp)

            console.log(jsonMockResp)
            setMockInterviewQuestion(jsonMockResp);
            setInterviewData(result[0]);
        } catch (error) {
            console.error("Error fetching interview details:", error);
            toast.error("Failed to load interview details");
        }
    }

    const handleEndInterview = async () => {
        setIsEnding(true);
        try {
            // Perform any necessary operations before ending the interview
            // For example, saving the final answer, updating interview status, etc.
            // await someAsyncOperation();

            // Navigate to the feedback page
            router.push(`/dashboard/interview/${interviewData?.mockId}/feedback`);
        } catch (error) {
            console.error("Error ending interview:", error);
            toast.error("Failed to end interview. Please try again.");
        } finally {
            setIsEnding(false);
        }
    };

    return (
        <div>
            <div className='grid grid-cols-1 md:grid-cols-2 gap-10'>
                <QuestionsSection 
                    mockInterviewQuestion={mockInterviewQuestion}
                    activeQuestionIndex={activeQuestionIndex}
                />
                <RecordAnswerSection
                    mockInterviewQuestion={mockInterviewQuestion}
                    activeQuestionIndex={activeQuestionIndex}
                    interviewData={interviewData}
                />
            </div>
            <div className='flex justify-end gap-6 text-primary'>
                {activeQuestionIndex > 0 &&   
                    <Button onClick={() => setActiveQuestionIndex(activeQuestionIndex - 1)}>Previous Question</Button>
                }
                {activeQuestionIndex !== mockInterviewQuestion?.length - 1 && 
                    <Button onClick={() => setActiveQuestionIndex(activeQuestionIndex + 1)}>Next Question</Button>
                }
                {activeQuestionIndex === mockInterviewQuestion?.length - 1 &&  
                    <Button onClick={handleEndInterview} disabled={isEnding}>
                        {isEnding ? 'Ending Interview...' : 'End Interview'}
                    </Button>
                }
            </div>
        </div>
    )
}

export default StartInterview