from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

class AnalysisAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-4", openai_api_key=self.api_key)
        else:
            self.llm = None
            print("Warning: OpenAI API Key not found. AnalysisAgent will return mock responses.")

    def summarize_findings(self, data):
        """
        Summarizes the findings from the analytics module.
        data: dictionary with flood, fire, and urban growth results.
        """
        if not self.llm:
            return f"Mock Summary: Detected {data.get('flood_area', 0)} sq km of flood and {data.get('urban_growth', 0)}% urban growth."

        template = """
        You are a Geospatial Intelligence Analyst. 
        Based on the following data detected from satellite imagery:
        - Flood Area: {flood_area} sq km
        - Urban Growth: {urban_growth}%
        - Vegetation Loss: {veg_loss}%
        - Wildfire Detected: {wildfire}
        
        Provide a concise technical summary of the environmental and urban state of the region.
        """
        
        prompt = PromptTemplate(template=template, input_variables=["flood_area", "urban_growth", "veg_loss", "wildfire"])
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        response = chain.run(
            flood_area=data.get('flood_area', 0),
            urban_growth=data.get('urban_growth', 0),
            veg_loss=data.get('veg_loss', 0),
            wildfire=data.get('wildfire', False)
        )
        
        return response

if __name__ == "__main__":
    agent = AnalysisAgent()
    data = {"flood_area": 12.4, "urban_growth": 25, "veg_loss": 11, "wildfire": True}
    print(agent.summarize_findings(data))
