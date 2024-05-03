import streamlit as st
from openai import OpenAI

class ConversationMemory:
    def __init__(self):
        self.memory = []

    def add_interaction(self, role, content):
        self.memory.append({"role": role, "content": content})

    def get_memory(self):
        return self.memory

def main():
    st.title("Ikigai Students")

    role_iki = """
    IkigAI specializes in vocational guidance for students transitioning from secondary school to university, using the Ikigai philosophy. 
    This GPT asks targeted questions to understand students' interests, skills and values, helping them to find their vocation and the most advisable university course. 
    The number of questions is limited to 15-20, with each question being progressively more specific to narrow down the topic until identifying the user's vocation, which can consist of several options. 
    IkigAI answers in Portuguese when asked in Portuguese and in English when asked in English. It uses direct and careful language, adapted for young people, being empathetic and detailed in its questions and suggestions, ensuring that students feel heard and understood. 
    The GPT guides users through the process with increasingly pertinent questions, allowing for personalized follow-up focused on the user's progress.
    """

    welcome_message = "Hi, I'm Iki Chat, your vocational guidance assistant!\n\nLet's discover your vocation together.\n\nThink about the activities you do, both at school and in your spare time. What are the ones you're good at and enjoy?"
    st.write(welcome_message)

    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationMemory()

    client = OpenAI()  # Initialize the OpenAI client

    user_input = st.text_input("Type your answer:")

    if st.button('Process') and user_input:
        if user_input.lower() == 'exit':
            st.stop("Thank for using IkiChat!")
        else:
            memory = st.session_state.memory
            messages = memory.get_memory() + [
                {"role": "system", "content": role_iki},
                {"role": "user", "content": user_input}
            ]
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            response = completion.choices[0].message.content.replace("\n", " ")
            st.write(response)
            # Add the current interaction to memory
            memory.add_interaction("user", user_input)
            memory.add_interaction("system", response)

if __name__ == "__main__":
    main()
