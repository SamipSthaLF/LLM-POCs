from langchain_community.llms import OpenAI
from openai import OpenAI
import numpy as np
from typing import List, Dict, Any
from stylemail.vectorstore import UserVectorStore

class EmailGenerator:
    def __init__(self, openai_api_key: str, vector_store: UserVectorStore):
        """
        Initialize the EmailGenerator with OpenAI API key and a vector store for user embeddings.
        
        Args:
            openai_api_key (str): The API key for OpenAI.
            vector_store (UserVectorStore): The vector store instance for user embeddings.
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store

    def embed_prompt(self, prompt: str) -> List[float]:
        """
        Generate an embedding for the given prompt using the OpenAI API.
        
        Args:
            prompt (str): The input prompt to embed.
        
        Returns:
            List[float]: The embedding vector for the prompt.
        
        Raises:
            RuntimeError: If the embedding request fails.
        """
        try:
            response = self.client.embeddings.create(
                input=[prompt],
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Failed to embed prompt with OpenAI API: {e}")

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """
        Compute the cosine similarity between two embedding vectors.
        
        Args:
            a (List[float]): First embedding vector.
            b (List[float]): Second embedding vector.
        
        Returns:
            float: Cosine similarity score between the two vectors.
        """
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

    def retrieve_style_context(self, user_id: str, prompt_embedding: List[float], top_k: int = 3) -> List[str]:
        """
        Retrieve top-k most similar writing samples from Redis based on prompt embedding.
        """
        entries = self.vector_store.get_all_embeddings(user_id)
        scored = [
            (self.cosine_similarity(prompt_embedding, e["embedding"]), e["text"])
            for e in entries
        ]
        scored.sort(reverse=True)
        return [text for _, text in scored[:top_k]]

    def build_prompt(self, context_samples: List[str], user_prompt: str) -> str:
        """
        Construct a prompt for the LLM using retrieved style samples and the user prompt.
        """
        context_block = "\n\n".join(context_samples)
        return (
            "You are an assistant that writes emails in the user's personal style.\n\n"
            "Here are some examples of the user's writing style:\n\n"
            f"{context_block}\n\n"
            "Now write an email based on the following prompt:\n\n"
            f"{user_prompt}"
        )

    def generate_email(self, user_id: str, subject: str, user_prompt: str) -> Dict[str, str]:
        """
        Generate an email in the user's style based on the subject and user prompt.
        
        Args:
            user_id (str): The user's unique identifier.
            subject (str): The subject of the email.
            user_prompt (str): The prompt or content for the email.
        
        Returns:
            Dict[str, str]: A dictionary containing the generated email subject and body.
        
        Raises:
            RuntimeError: If no style data is found or the OpenAI API call fails.
        """
        full_input = f"Subject: {subject}\n\n{user_prompt}"
        prompt_embedding = self.embed_prompt(full_input)
        context = self.retrieve_style_context(user_id, prompt_embedding)
        if not context:
            raise RuntimeError(f"No style data found for user '{user_id}'. Please seed user style first.")
        full_prompt = self.build_prompt(context, f"Subject: {subject}\n\n{user_prompt}")
        print("[generate_email] Full prompt sent to OpenAI:\n", full_prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return {"subject": "Generated Email", "body": content}
        except Exception as e:
            raise RuntimeError(f"Failed to generate email with OpenAI API: {e}")
class NudgeSummaryGenerator:
    def __init__(self, openai_api_key: str, vector_store: UserVectorStore):
        """
        Initialize the NudgeSummaryGenerator with OpenAI API key and a vector store for user embeddings.
        
        Args:
            openai_api_key (str): The API key for OpenAI.
            vector_store (UserVectorStore): The vector store instance for user embeddings.
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store

    def generate_summary(self, user_id: str, prompt: str, nudges: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Generate a summary for the given nudges based on the prompt.
        
        Args:
            user_id (str): The user's unique identifier.
            prompt (str): The prompt for generating the summary.
            nudges (List[Dict[str, str]]): A list of nudges to be summarized.
        
        Returns:
            Dict[str, str]: A dictionary containing the generated summary.
        
        Raises:
            RuntimeError: If the OpenAI API call fails.
        """
        # Example implementation, adjust as needed
        full_prompt = f"Prompt: {prompt}\n\nNudges:\n" + "\n".join(
            f"Title: {n['title']}, Instructions: {n['instructions']}, Metrics: {n['metrics']}"
            for n in nudges
        )
        print("[generate_summary] Full prompt sent to OpenAI:\n", full_prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return {"summary": content}
        except Exception as e:
            raise RuntimeError(f"Failed to generate summary with OpenAI API: {e}")
class NudgeEmailGenerator:
    def __init__(self, openai_api_key: str, vector_store: UserVectorStore):
        """
        Initialize the NudgeEmailGenerator with OpenAI API key and a vector store for user embeddings.
        
        Args:
            openai_api_key (str): The API key for OpenAI.
            vector_store (UserVectorStore): The vector store instance for user embeddings.
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store

    def generate_email(self, user_id: str, prompt: str, nudges: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Generate an email for the given nudges based on the prompt.
        
        Args:
            user_id (str): The user's unique identifier.
            prompt (str): The prompt for generating the email.
            nudges (List[Dict[str, str]]): A list of nudges to be included in the email.
        
        Returns:
            Dict[str, str]: A dictionary containing the generated email subject and body.
        
        Raises:
            RuntimeError: If the OpenAI API call fails.
        """
        nudge_texts = "\n\n".join(
            f"Title: {n['title']}\nInstructions: {n['instructions']}\nMetrics: {n['metrics']}"
            for n in nudges
        )
        full_prompt = (
            f"{prompt}\n\n"
            f"Nudges for the Employee Sally:\n{nudge_texts}\n\n"
            "Write a complete and polished email to the employee addressing the nudges. "
            "The email should be professional, concise, and provide clear next steps."
            "The nudges are things the writer needs to do for their team member and this email is them addressing them and reaching out to their team member."
        )

        print("[generate_email] Full prompt sent to OpenAI:\n", full_prompt)
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
            )
            content = response.choices[0].message.content
            # Assuming the response content is structured with a subject and body
            lines = content.split("\n")
            subject_line = next((line for line in lines if line.lower().startswith("subject:")), "Subject: No Subject")
            subject = subject_line.split(":", 1)[1].strip() if ":" in subject_line else "No Subject"
            body = "\n".join(line for line in lines if not line.lower().startswith("subject:"))
            return {"subject": subject, "body": body}
        except Exception as e:
            raise RuntimeError(f"Failed to generate nudge email with OpenAI API: {e}")
