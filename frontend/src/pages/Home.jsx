import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import api from "../services/api";

import "../styles/Home.css";

function Home() {

  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "Welcome to Research Copilot! Ask me anything about your research papers."
    }
  ]);

  const [loading, setLoading] = useState(false);

  const askQuestion = async (question) => {

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: question
      }
    ]);

    setLoading(true);

    try {

      const response = await api.post("/chat", {
        question
      });

      setMessages(prev => [
        ...prev,
        {
          sender: "assistant",
          text: response.data.answer,
          sources: response.data.sources
        }
      ]);

    } catch (error) {

      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: "Failed to connect to backend."
        }
      ]);

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="app">

      <Navbar />

      <div className="content">

        <Sidebar />

        <div className="chat-section">

          <ChatWindow
            messages={messages}
            loading={loading}
          />

          <ChatInput
            onSend={askQuestion}
          />

        </div>

      </div>

    </div>

  );

}

export default Home;

