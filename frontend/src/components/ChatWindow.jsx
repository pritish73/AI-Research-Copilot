import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatWindow({ messages, loading }) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages, loading]);

    return (

        <div className="chat-window">

            {messages.map((msg, index) => (

                <Message
                    key={index}
                    sender={msg.sender}
                    text={msg.text}
                    sources={msg.sources}
                   
                />

            ))}

            {
                loading && (

                    <Message
                        sender="assistant"
                        text=" Thinking..."
                    />

                )
            }


            <div ref={bottomRef}></div>

        </div>

    );

}

export default ChatWindow;