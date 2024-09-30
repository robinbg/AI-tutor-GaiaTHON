# AI Learning Assistant

This project is an entry for the Living Knowledge Systems - Decentralized AI Hackathon.

## Purpose

The AI Learning Assistant is designed to assess and teach users about their chosen topics. It uses advanced AI models to evaluate prerequisite knowledge, provide feedback, and guide users through a structured learning process.

## Features

- **Topic Selection**: Users can specify the topic they want to learn about.
- **Knowledge Assessment**: The AI asks targeted questions to assess the user's prerequisite knowledge.
- **Feedback and Guidance**: Provides feedback on user responses and suggests a teaching strategy.
- **Teaching Steps**: Guides users through learning steps with clear explanations and thought-provoking questions.
- **Personalized Learning**: Through three assessment questions, the AI not only gauges the user's knowledge level but also understands their teaching style preferences, allowing it to adjust the teaching language and style accordingly.

## How to Run

1. **Install Dependencies**: Ensure you have Python and Streamlit installed. You can install the required packages using:
    ```bash
    pip install streamlit langchain_openai
    ```

2. **Run the Application**: Execute the following command to start the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Screenshots

### 1. Home Screen
![Home Screen](asset/shot1.jpg)
*Description: The home screen where users can enter the topic they want to learn about.*

### 2. Knowledge Assessment
![Knowledge Assessment](path/to/screenshot2.png)
*Description: The AI asks targeted questions to assess the user's prerequisite knowledge.*

### 3. Feedback and Guidance
![Feedback and Guidance](path/to/screenshot3.png)
*Description: The AI provides feedback on user responses and suggests a teaching strategy.*

### 4. Teaching Steps
![Teaching Steps](path/to/screenshot4.png)
*Description: The AI guides users through learning steps with clear explanations and thought-provoking questions.*

### 5. Personalized Learning
![Personalized Learning](path/to/screenshot5.png)
*Description: The AI adjusts the teaching language and style based on the user's preferences.*

## Usage

1. Start the application.
2. Enter the topic you want to learn about.
3. Answer the AI's questions to assess your knowledge.
4. Receive feedback and follow the teaching steps provided by the AI.

## Acknowledgements

This project utilizes the following technologies:
- [Streamlit](https://streamlit.io/): For building the web interface.
- [Langchain OpenAI](https://github.com/langchain-ai/langchain): For AI model integration.
- [Gaianet](https://gaianet.ai): For providing the base URL for the AI model.

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

