# MicroIntent

**An Intent-Based Placement Strategy Generation Framework for Microservice Applications in the Compute Continuum Using LLMs**

<img width="773" height="440" alt="MicroIntent Screenshot" src="https://github.com/user-attachments/assets/5d6eca72-e628-4ead-a3c3-c11f83a3bc08" />

---

## Overview
MicroIntent is a framework designed to generate placement strategies for microservice applications across the compute continuum (edge, fog, and cloud) based on high-level, natural language intents. It leverages Large Language Models (LLMs) to interpret user intents and produce optimal deployment strategies.

---

## Tutorial & Demonstration
A **video tutorial** is available to demonstrate the MVP, including reproducibility of our evaluation and step-by-step installation in a Docker container.

**Tutorial link:** [Watch the sample tutorial](https://drive.google.com/file/d/1UJ0CtBP7Ar97t_qTIOyElT7lByyDCVj-/view?usp=sharing)

> **Note:**  
> The API key shown in the video has been replaced for security purposes. Please use your own API key for your preferred LLM provider by configuring the `intent_parser.py` file in the backend folder.

---

## Prerequisites
- **Docker** must be installed on your machine.

---

## Installation & Running the MVP

1. **Clone the repository**  
   ```bash
   git clone https://github.com/koushikur-islam/MicroIntent/
   cd MicroIntent
   ```

2. **Configure your API key**  
   - Open `intent_parser.py` located in the `back-end` folder.  
   - On **line 4**, replace the placeholder with your LLM API key (e.g., OpenAI API key).  
   - Save the file.

3. **Start the application with Docker**  
   ```bash
   docker compose up -d
   ```

4. **Access the web application**  
   - Open a browser and navigate to:  
     [http://localhost:3000](http://localhost:3000)

5. **Upload your infrastructure description**  
   - Use the sample JSON file in the `sample` folder as a template.  
   - You can modify this file, but ensure the structure remains intact.

6. **Add service-tagged intents**  
   - Click **"Add Intent"** in the UI.  
   - You can use the sample `intents.txt` file from the `sample` folder.

7. **Generate placement decisions**  
   - Click **"Generate"** to view the placement strategy output.

---

## Notes
- Ensure the infrastructure JSON file follows the required schema for correct processing.  
- You can adapt the intents to your own use case, provided they are written in natural language.
