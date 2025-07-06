import os

# Root path (change only if your folder location changes)
BASE_DIR = r"C:\Users\yoges\projects\AI_Implementation_Intelligence_Platform-beaconAI"

# Folder and file structure
structure = {
    "api/routes": ["intake.py", "insight.py", "report.py", "email.py"],
    "api/schemas": ["intake_schema.py", "response_schema.py"],
    "api/utils": ["prompt_builder.py", "logger.py"],
    "api": ["main.py"],
    "scraper": ["goose_scraper.py", "selenium_scraper.py", "cleaner.py"],
    "llm_engine": ["llama_client.py", "prompt_template.py", "rag_engine.py"],
    "vector_store": ["embedder.py", "faiss_index.py", "formatter.py"],
    "reporting": ["pdf_builder.py", "template_loader.py", "utils.py"],
    "email_service": ["sendgrid_client.py", "mailgun_client.py"],
    "email_service/templates": ["email_body.html"],
    "frontend/public": [".gitkeep"],
    "frontend/components": ["IntakeForm.tsx", "DownloadCard.tsx"],
    "frontend/pages": ["index.tsx", "success.tsx"],
    "frontend/utils": ["api.ts"],
    "frontend/styles": ["theme.css"],
    "config": ["settings.py", ".env.example"],
    "tests": [
        "test_scraper.py", "test_llm_client.py", "test_prompt_logic.py",
        "test_faiss.py", "test_pdf_builder.py"
    ],
    "deployment": [
        "Dockerfile", "docker-compose.yml", "start.sh", "Procfile", "README.md"
    ],
}

def create_structure(base_path, structure_dict):
    for folder, files in structure_dict.items():
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")
                print(f"✅ Created: {file_path}")
            else:
                print(f"⚠️ Already exists: {file_path}")

if __name__ == "__main__":
    print(f"\n📂 Creating structure in: {BASE_DIR}")
    create_structure(BASE_DIR, structure)
    print("\n✅ Folder structure creation completed!")
