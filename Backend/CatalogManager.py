from typing import List

class CatalogManager():
    def __init__(self):
        pass

    def get_chapter_list(self, prompt: str) -> List[str]:
        pass

    def get_chapter_content(self,prompt:str) -> List[str] : #Gives [chapter_title,chapter_content]
        pass

    def give_modified_chapter(self,content:str) -> str :
        pass

    def modify_json(self,chapter_title:str,new_chapter_content:str):
        pass