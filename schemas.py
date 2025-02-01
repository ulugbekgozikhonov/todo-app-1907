from pydantic import BaseModel,Field

class CreateTodoSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    priority: int = Field(...)
    # completed: bool = Field(default=False)
    user_id: int = Field(...)
    
class CreateUserSchema(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)
    
class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)