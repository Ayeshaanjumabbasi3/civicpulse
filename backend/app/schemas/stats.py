from pydantic import BaseModel
from app.models.enums import Category, Priority, Status
class StatsResponse(BaseModel): total:int; by_category:dict[Category,int]; by_priority:dict[Priority,int]; by_status:dict[Status,int]; resolved:int
