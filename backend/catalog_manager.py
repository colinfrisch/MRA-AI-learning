from typing import List
import json



class CatalogManager():
    def __init__(self):
        with open('data/chapters_extended.json', 'r') as file:
            self.chapters = json.load(file)["chapters"]
        pass

    def get_chapter_list(self) -> List[str]:
        return [str(chapter['name'])+' - '+str(chapter['description']) for chapter in self.chapters]

    def get_chapter_content(self,chapter_title:str) -> str :
        return [chapter['content'] for chapter in self.chapters if chapter['name'] == chapter_title][0]
        

    def modify_chapter(self,chapter_title:str,new_chapter_content:str) :
        [chapter.update({'content':new_chapter_content}) for chapter in self.chapters if chapter['name'] == chapter_title]
        
        # Save the new chapters list in test file
        with open('data/chapters_extended_test.json', 'w') as file:
            json.dump({"chapters":self.chapters}, file)
        
        return self.chapters
