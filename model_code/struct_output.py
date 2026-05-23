from init_llm import ark_llm
from pydantic import BaseModel,Field

class Person(BaseModel):
    name:str=Field(description="姓名")
    age:int=Field(description="年龄")
    email:str=Field(description="邮箱")

model_with_structured_output = ark_llm.with_structured_output(Person)

if __name__=="__main__":
    # print(ark_llm.invoke("介绍一下你自己"))
    resp=model_with_structured_output.invoke("请介绍一个25岁的张三")
    print(resp)
    print(resp.name)
    print(resp.age)
    print(resp.email)
