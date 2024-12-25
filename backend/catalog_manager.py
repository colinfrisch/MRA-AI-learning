from typing import List
import json



class CatalogManager():
    def __init__(self):
        pass

    def get_chapter_list(self) -> List[str]:
        with open('../data/chapters_extended.json', 'r') as file:
            chapters = json.load(file)["chapters"]

        return [str(chapter['name'])+' - '+str(chapter['description']) for chapter in chapters]

    def get_chapter_content(self,chapter_title:str) -> str :
        with open('../data/chapters_extended.json', 'r') as file:
            chapters = json.load(file)["chapters"]
        return [chapter['content'] for chapter in chapters if chapter['name'] == chapter_title][0]
        

    def modify_chapter(self,chapter_title:str,new_chapter_content:str) :
        pass
