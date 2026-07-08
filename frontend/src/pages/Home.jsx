import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import SuggestionChips from "../components/SuggestionChips";
import api from "../services/api";

import "../styles/Home.css";

function Home() {

    const [chats, setChats] = useState([
        {
            id: 1,
            title: "New Chat",
            messages: [
                {
                    sender: "assistant",
                    text: "Welcome to Research Copilot! Ask me anything about your research papers."
                }
            ]
        }
    ]);

    const [currentChatId, setCurrentChatId] = useState(1);

    const [loading, setLoading] = useState(false);

    const currentChat = chats.find(
        chat => chat.id === currentChatId
    );

    function updateCurrentChat(messages) {

        setChats(prevChats =>
            prevChats.map(chat =>
                chat.id === currentChatId
                    ? {
                        ...chat,
                        messages
                    }
                    : chat
            )
        );

    }

    function renameCurrentChat(title) {

        setChats(prev =>

            prev.map(chat =>

                chat.id === currentChatId

                    ? {
                        ...chat,
                        title
                    }

                    : chat

            )

        );

    }

    function createNewChat() {

        const newChat = {

            id: Date.now(),

            title: "New Chat",

            messages: [
                {
                    sender: "assistant",
                    text: "Welcome to Research Copilot! Ask me anything about your research papers."
                }
            ]

        };

        setChats(prev => [

            newChat,

            ...prev

        ]);

        setCurrentChatId(newChat.id);

    }

    function deleteChat(chatId) {

        const updatedChats = chats.filter(
            chat => chat.id !== chatId
        );

        // If the last chat was deleted, create a new one
        if (updatedChats.length === 0) {

            const newChat = {
                id: Date.now(),
                title: "New Chat",
                messages: [
                    {
                        sender: "assistant",
                        text: "Welcome to Research Copilot! Ask me anything about your research papers."
                    }
                ]
            };

            setChats([newChat]);
            setCurrentChatId(newChat.id);

            return;
        }

        setChats(updatedChats);

        // If the deleted chat was active, switch to the first remaining chat
        if (currentChatId === chatId) {

            setCurrentChatId(updatedChats[0].id);

        }

    }

    const askQuestion = async (question) => {

        const userMessage = {
            sender: "user",
            text: question
        };

        if (currentChat.title === "New Chat") {

            let title = question.trim();

            const words = title.split(" ");

            if (words.length > 6) {

                title = words.slice(0,6).join(" ") + "...";

            }

            renameCurrentChat(title);

        }

        const updatedMessages = [
            ...currentChat.messages,
            userMessage
        ];

        updateCurrentChat(updatedMessages);

        setLoading(true);

        try {

            const response = await api.post("/chat", {
                question
            });

            updateCurrentChat([
                ...updatedMessages,
                {
                    sender: "assistant",
                    text: response.data.answer,
                    sources: response.data.sources
                }
            ]);

        }

        catch (error) {

            updateCurrentChat([
                ...updatedMessages,
                {
                    sender: "assistant",
                    text: "Failed to connect to backend."
                }
            ]);

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="app">

            <Navbar />

            <div className="content">

                <Sidebar
                    chats={chats}
                    currentChatId={currentChatId}
                    setCurrentChatId={setCurrentChatId}
                    createNewChat={createNewChat}
                    deleteChat={deleteChat}
                />

                <div className="chat-section">

                     <ChatWindow
                        messages={currentChat.messages}
                        loading={loading}
                    />

                    {currentChat.messages.length === 1 && (

                    <SuggestionChips
                        onSelect={askQuestion}
                    />

                )}

                    <ChatInput
                        onSend={askQuestion}
                    />

                </div>

            </div>

        </div>

    );

}

export default Home;