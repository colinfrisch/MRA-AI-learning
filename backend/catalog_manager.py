from typing import List
import json



class CatalogManager():
    def __init__(self):
        pass

    def get_chapter_list(self) -> List[str]:
        with open('data/chapters.json', 'r') as file:
            chapters = json.load(file)["chapters"]

        return [str(chapter['name'])+' - '+str(chapter['description']) for chapter in chapters]

    def get_chapter_title(self,prompt:str) -> str :
        pass

    def get_chapter_content(self,prompt:str) -> str : 
        pass

    def modify_chapter(self,chapter_title:str,new_chapter_content:str) :
        pass
