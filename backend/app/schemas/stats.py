from pydantic import BaseModel
from app.models.enums import Category, Priority
class StatsResponse(BaseModel): total:int; by_category:dict[Category,int]; by_priority:dict[Priority,int]; resolved:int
