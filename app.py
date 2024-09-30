import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import re

model = ChatOpenAI(model="Llama-3-8B-Instruct", api_key="nokey", base_url="https://llama3.us.gaianet.network/v1")

assessment_prompt = """As an AI learning assistant, assess the user's prerequisite knowledge for their chosen topic:

1. Ask ONE specific question on key prerequisites directly related to the topic.
2. Cover only fundamental knowledge necessary for understanding the topic.
3. Encourage detailed responses; avoid yes/no questions.
4. Design questions to easily evaluate understanding.
5. Progress from advanced to basic concepts if needed.
6. Max 3 questions total.
7. Stick to existing knowledge; don't introduce new concepts.
8. For the final question, provide feedback without asking further questions.
9. Stay focused on the topic and its direct prerequisites.

Ask one question at a time. Maintain a friendly, supportive tone."""

def main():
    st.title("AI Learning Assistant")
    chat()

def chat():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.stage = "topic_selection"
        st.session_state.assessment_question_count = 0
        st.session_state.initial_topic = None
        st.session_state.teaching_step = 0  # Initialize teaching step
        initial_message = "Welcome! What topic would you like to learn about?"
        st.session_state.messages.append(AIMessage(content=initial_message))

    for message in st.session_state.messages:
        with st.chat_message(message.type):
            st.markdown(message.content)

    if user_input := st.chat_input("Your response:"):
        response = ""
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.chat_message("human"):
            st.markdown(user_input)

        if st.session_state.stage == "topic_selection":
            st.session_state.initial_topic = extract_topic(user_input)
            st.session_state.stage = "assessment"
            st.session_state.assessment_question_count = 0
        
        if st.session_state.stage == "assessment":
            if st.session_state.assessment_question_count > 0:
                response += generate_assessment_feedback(st.session_state.initial_topic, st.session_state.messages[-2:])
                response += "\n\n"
            
            if st.session_state.assessment_question_count < 3:
                response += generate_assessment_question(st.session_state.initial_topic, 
                                                         st.session_state.assessment_question_count + 1, 
                                                         st.session_state.messages)
                st.session_state.assessment_question_count += 1
            else:
                user_feedback, teaching_guidance = generate_comprehensive_assessment(st.session_state.messages)
                response += "\n\n" + user_feedback
                st.session_state.teaching_guidance = teaching_guidance
                st.session_state.stage = "teaching"
        if st.session_state.stage == "teaching":
            if st.session_state.teaching_step == 0:
                if response is not None and len(response) > 0:
                    response += "\n\n"  
                else:
                    response = ""
                response += generate_teaching_response(st.session_state.initial_topic, st.session_state.teaching_guidance, 1, st.session_state.messages)
                st.session_state.teaching_step = 1
            else:
                if response is not None and len(response) > 0:
                    response += "\n\n"  
                else:
                    response = ""
                response += generate_teaching_response(st.session_state.initial_topic, "", st.session_state.teaching_step + 1, st.session_state.messages)
                st.session_state.teaching_step += 1

        st.session_state.messages.append(AIMessage(content=response))
        with st.chat_message("ai"):
            st.markdown(response)
          

def generate_response(messages):
    try:
        response = model.invoke(messages)
        return response.content
    except Exception as e:
        st.error(f"Error: {e}")
        return "I apologize, but an error occurred while generating the response."

def generate_comprehensive_assessment(messages):
    user_feedback_prompt = f"""Based on our conversation about {st.session_state.initial_topic}, please provide:

1. A brief, conversational summary of the user's prerequisite knowledge.
2. A concise evaluation of their readiness to learn {st.session_state.initial_topic}.
3. An encouraging statement about moving forward with the topic.

Keep your tone warm and supportive. Focus on providing a clear picture of the user's current knowledge state and readiness to learn. Avoid formal headings or sections."""

    teaching_guidance_prompt = f"""Based on the same conversation and assessment, please provide:

1. A brief overview of the user's knowledge gaps or areas that need reinforcement.
2. Suggestions for the most effective teaching approach for this user, considering their current understanding.
3. Recommendations for key concepts to focus on initially when teaching {st.session_state.initial_topic}.

This guidance should be concise and focused on informing the teaching strategy."""

    messages_for_user_feedback = [
        *messages,
        HumanMessage(content=user_feedback_prompt),
    ]
    messages_for_teaching_guidance = [
        *messages,
        HumanMessage(content=teaching_guidance_prompt),
    ]

    try:
        user_feedback = model.invoke(messages_for_user_feedback).content
        teaching_guidance = model.invoke(messages_for_teaching_guidance).content
        return user_feedback, teaching_guidance
    except Exception as e:
        st.error(f"Error: {e}")
        return (f"Great! Based on our conversation, you seem well-prepared to start learning about {st.session_state.initial_topic}. Let's begin our exciting journey into this subject!",
                f"Focus on introducing basic concepts of {st.session_state.initial_topic} and build upon the user's existing knowledge.")

def generate_teaching_response(topic, comprehensive_assessment, teaching_step, message_history):
    system_prompt = f"""You are an enthusiastic and knowledgeable AI tutor teaching about {topic}. 
    Use the following assessment to guide your teaching:
    {comprehensive_assessment}
    
    For each teaching step:
    1. Introduce or build upon fundamental concepts of {topic}.
    2. Provide clear explanations with relatable examples.
    3. Include real-world applications when possible.
    4. End each response with a thought-provoking question to encourage further discussion.
    
    Maintain a friendly and conversational tone throughout the interaction."""

    messages = [
        SystemMessage(content=system_prompt),
        *message_history
    ]

    if teaching_step == 1:
        messages.append(HumanMessage(content=f"Let's start our lesson on {topic}. What's the first thing we should know?"))
    else:
        messages.append(HumanMessage(content=f"What's the next important concept we should cover in {topic}?"))

    try:
        response = model.invoke(messages)
        content = response.content
        
       
        return content
    except Exception as e:
        st.error(f"Error: {e}")
        return f"I apologize, but I'm having trouble generating a response about {topic}. What would you like to know more about?"

def generate_assessment_question(topic, question_number, message_history):
    
    try:
        response = model.invoke([SystemMessage(content=assessment_prompt), *message_history[1:]])
        return response.content
    except Exception as e:
        st.error(f"Error: {e}")
        return f"I apologize, but I'm having trouble generating a question about {topic}. Could you please share what you know about this subject?"

def format_message_history(messages):
    formatted_history = ""
    for msg in messages:
        role = "Human" if isinstance(msg, HumanMessage) else "AI"
        formatted_history += f"{role}: {msg.content}\n\n"
    return formatted_history

def generate_assessment_feedback(topic, last_messages):
    prompt = f"""Provide feedback on the user's answer about {topic}:

1. Be specific and relate to the user's answer.
2. Highlight correct aspects.
3. Gently point out misconceptions or areas for improvement.
4. Offer brief clarification if needed.
5. Don't introduce new concepts related to {topic}.
6. Don't end with a question.
7. Keep feedback concise, focused on existing knowledge."""
    messages = [
        SystemMessage(content=prompt),
        *last_messages
    ]
    
    try:
        response = model.invoke(messages)
        filtered_content = remove_ending_questions(response.content)
        print(filtered_content)
        return filtered_content
    except Exception as e:
        st.error(f"Error: {e}")
        return f"Thank you for your response about {topic}. Let's move on to the next part of our discussion."

def remove_ending_questions(text):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Remove consecutive questions from the end
    while sentences and re.search(r'\?\s*$', sentences[-1]):
        sentences.pop()
    
    return ' '.join(sentences).strip()

def extract_topic(user_input):
    prompt = f"""Given the following user input, extract and return only the main topic the user wants to learn about. 
    The response should be a short phrase or single word representing the core subject.
    Do not include any explanation or additional text in your response.

    User input: "{user_input}"

    Topic:"""

    try:
        response = model.invoke([HumanMessage(content=prompt)])
        print(response)
        topic = response.content.strip()
        # Capitalize the first letter of each word
        topic = ' '.join(word.capitalize() for word in topic.split())
        return topic
    except Exception as e:
        st.error(f"Error in topic extraction: {e}")
        return user_input  # 如果出错，返回原始输入

if __name__ == "__main__":
    main()