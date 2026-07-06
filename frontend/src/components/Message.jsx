import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

function Message({ sender, text, sources }) {

    const [displayedText, setDisplayedText] = useState(
        sender === "user" ? text : ""
    );

    useEffect(() => {

        if (sender === "user") {
            setDisplayedText(text);
            return;
        }

        let index = 0;

        setDisplayedText("");

        const interval = setInterval(() => {

            index++;

            setDisplayedText(
                text.slice(0, index)
            );

            if (index >= text.length) {

                clearInterval(interval);

            }

        }, 12);

        return () => clearInterval(interval);

    }, [text, sender]);

    return (

        <div className={`message ${sender}`}>

            <div className="bubble">

                <ReactMarkdown>
                    {displayedText}
                </ReactMarkdown>

                {
                    sender === "assistant" &&
                    sources &&
                    displayedText.length === text.length &&
                    sources.length > 0 &&

                    <div className="sources">

                        <h4>Sources</h4>

                        {
                            sources.map((source, index) => (

                                <div
                                    key={index}
                                    className="source-card"
                                >
                                    📄 {source}
                                </div>

                            ))
                        }

                    </div>

                }

            </div>

        </div>

    );

}

export default Message;