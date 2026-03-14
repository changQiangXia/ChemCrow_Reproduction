import os

from langchain import agents
from langchain.base_language import BaseLanguageModel

from chemcrow.tools import *


def make_tools(llm: BaseLanguageModel, api_keys: dict = {}, local_rxn: bool=False, verbose=True):
    serp_api_key = api_keys.get("SERP_API_KEY") or os.getenv("SERP_API_KEY")
    rxn4chem_api_key = api_keys.get("RXN4CHEM_API_KEY") or os.getenv("RXN4CHEM_API_KEY")
    rxn4chem_project_id = api_keys.get("RXN4CHEM_PROJECT_ID") or os.getenv("RXN4CHEM_PROJECT_ID")
    openai_api_key = api_keys.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    openai_api_base = api_keys.get("OPENAI_API_BASE") or os.getenv("OPENAI_API_BASE")
    summary_model = api_keys.get("CHEMCROW_SUMMARY_MODEL") or os.getenv("CHEMCROW_SUMMARY_MODEL")
    chemspace_api_key = api_keys.get("CHEMSPACE_API_KEY") or os.getenv(
        "CHEMSPACE_API_KEY"
    )
    semantic_scholar_api_key = api_keys.get("SEMANTIC_SCHOLAR_API_KEY") or os.getenv(
        "SEMANTIC_SCHOLAR_API_KEY"
    )

    all_tools = agents.load_tools(
        [
            "python_repl",
            # "human"
        ]
    )
    all_tools += [SafeWikipedia()]

    all_tools += [
        Query2SMILES(chemspace_api_key),
        Query2CAS(),
        SMILES2Name(),
        PatentCheck(),
        MolSimilarity(),
        SMILES2Weight(),
        FuncGroups(),
        ExplosiveCheck(),
        ControlChemCheck(),
        SimilarControlChemCheck(),
        SafetySummary(llm=llm),
        Scholar2ResultLLM(
            llm=llm,
            openai_api_key=openai_api_key,
            semantic_scholar_api_key=semantic_scholar_api_key,
        ),
    ]
    if chemspace_api_key:
        all_tools += [GetMoleculePrice(chemspace_api_key)]
    if serp_api_key:
        all_tools += [WebSearch(serp_api_key)]
    if (not local_rxn) and rxn4chem_api_key:
        all_tools += [
            RXNPredict(rxn4chem_api_key, project_id=rxn4chem_project_id),
            RXNRetrosynthesis(
                rxn4chem_api_key,
                openai_api_key,
                project_id=rxn4chem_project_id,
                summary_model=summary_model,
                openai_api_base=openai_api_base,
            ),
        ]
    elif local_rxn:
        all_tools += [
            RXNPredictLocal(),
            RXNRetrosynthesisLocal(
                openai_api_key=openai_api_key,
                summary_model=summary_model,
                openai_api_base=openai_api_base,
            ),
        ]

    return all_tools
