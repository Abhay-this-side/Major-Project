import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-100 to-green-100">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-md p-4">
        <div className="container mx-auto flex justify-center items-center">
          <Link href="/" className="text-center">
            <Image src={'/logo.svg'} width={160} height={100} alt='logo' />
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4 text-gray-800">Master Your Interviews with AI</h1>
          <p className="text-xl text-gray-600 mb-8">Prepare, practice, and perfect your interview skills with our cutting-edge AI technology</p>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { title: "AI-Powered Practice", icon: "🤖", description: "Get realistic interview simulations powered by advanced AI" },
            { title: "Personalized Feedback", icon: "📊", description: "Receive detailed feedback on your performance and areas for improvement" },
            { title: "Extensive Question Bank", icon: "📚", description: "Access a vast library of interview questions across various industries" },
          ].map((feature, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-lg text-center">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16">
          <h2 className="text-3xl font-bold mb-4 text-gray-800">Ready to Excel in Your Interviews?</h2>
          <Link href="/dashboard">
            <Button size="lg" className="bg-green-600 hover:bg-green-700 text-white">Start Practicing Now</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
