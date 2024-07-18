from enum import Enum

class DormList(Enum):
    """
    기숙사 = (한글 이름, Dorm.id)
    """
    ALL = ("전체 기숙사", 1)
    EAST = ("동서울관", 2)
    WEST = ("서서울관", 3)

    @property
    def id(self):
        """
        DormList.ALL.id = 1
        """
        return self.value[1]
    
    @property
    def dorm_name(self):
        """
        DormList.EAST.name = "동서울관"
        """
        return self.value[0]
    
    @classmethod
    def get_names(self):
        """
        DormList.get_names()
        = ('ALL', 'EAST', 'WEST')
        """
        return tuple(self._member_names_)
    
    @classmethod
    def get_values(self):
        """
        DormList.get_values()
        = (('전체 기숙사', 1), ('동서울관', 2), ('서서울관', 3))
        """
        return tuple(member.value for member in self)
    
    @classmethod
    def get_choices(self):
        """
        DormList.get_choices()
        = (('ALL', '전체 기숙사'), ('EAST', '동서울관'), ('WEST', '서서울관'))
        """
        return tuple((member.name, member.value[0]) for member in self)