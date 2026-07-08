import api from "../services/api";

function UploadButton({ onUpload }) {

    const uploadFile = async (event) => {

        const file = event.target.files[0];

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        try {

            await api.post("/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });

            alert("Paper uploaded successfully.");

            if (onUpload) {
                onUpload();
            }

        }

        catch (err) {

            console.error(err);

            alert("Upload failed.");

        }

    };

    return (

        <div>

            <label className="upload-btn">

                Upload PDF

                <input
                    type="file"
                    accept=".pdf"
                    hidden
                    onChange={uploadFile}
                    hidden
                />

            </label>

        </div>

    );

}

export default UploadButton;