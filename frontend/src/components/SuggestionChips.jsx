function SuggestionChips({ onSelect }) {

    const suggestions = [
        {
            label: "Summarize",
            prompt: "Summarize the uploaded research papers."
        },
        {
            label: "Compare Papers",
            prompt: "Compare the uploaded research papers."
        },
        {
            label: "Research Gaps",
            prompt: "Identify the research gaps in the uploaded papers."
        },
        {
            label: "Methodology",
            prompt: "Explain the methodology used in the uploaded papers."
        }
    ];

    return (

        <div className="suggestion-chips">

            {suggestions.map((item) => (

                <button
                    key={item.label}
                    className="chip"
                    onClick={() => onSelect(item.prompt)}
                >
                    {item.label}
                </button>

            ))}

        </div>

    );

}

export default SuggestionChips;