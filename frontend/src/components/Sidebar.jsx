import { useEffect, useState } from "react";
import api from "../services/api";
import UploadButton from "./UploadButton";
import { FaTrash } from "react-icons/fa";

function Sidebar() {

    const [papers, setPapers] = useState([]);

    const [stats, setStats] = useState({
        papers: 0,
        chunks: 0,
        vectors: 0
    });

    async function loadPapers() {

        try {

            const response = await api.get("/papers");

            setPapers(response.data.papers);

        }

        catch (err) {

            console.error(err);

        }

    }

    async function loadStats() {

        try {

            const response = await api.get("/stats");

            setStats(response.data);

        }

        catch (err) {

            console.error(err);

        }

    }

    useEffect(() => {

        loadPapers();
        loadStats();

    }, []);

    const deletePaper = async (paper) => {

        const confirmDelete = window.confirm(
            `Delete "${paper}"?`
        );

        if (!confirmDelete) return;

        try {

            await api.delete(`/paper/${encodeURIComponent(paper)}`);

            loadPapers();
            loadStats();

        }

        catch (err) {

            console.error(err);

            alert("Failed to delete paper.");

        }

    };

    return (

        <aside className="sidebar">

            <h2>Papers</h2>

            <div className="stats-card">

                <div className="stat-row">
                    <span>Papers</span>
                    <strong>{stats.papers}</strong>
                </div>

                <div className="stat-row">
                    <span>Chunks</span>
                    <strong>{stats.chunks}</strong>
                </div>

                <div className="stat-row">
                    <span>Vectors</span>
                    <strong>{stats.vectors}</strong>
                </div>

            </div>

            <UploadButton
                onUpload={() => {
                    loadPapers();
                    loadStats();
                }}
            />

            {
                papers.map((paper) => (

                    <div
                        className="paper"
                        key={paper}
                    >

                        <span>
                            📄 {paper}
                        </span>

                        <button
                            className="delete-btn"
                            onClick={(e) => {
                                e.stopPropagation();
                                deletePaper(paper);
                            }}
                        >
                            <FaTrash />
                        </button>

                    </div>

                ))
            }

        </aside>

    );

}

export default Sidebar;