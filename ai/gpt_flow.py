from ai.assistent import Assistent
import ai.prompts as prompts

class GPTFlow:
    def __init__(self, project_data: dict, project_images: list, assistant: Assistent):
        self.title = project_data['title']
        self.description = project_data['description']
        self.funnel_desc = project_data['funnel_desc']
        self.img_desc = project_data['img_desc']
        self.metric_title = project_data['metric_title']
        self.metric_desc = project_data['metric_desc']
        self.metric_target = project_data['metric_target']
        self.extra_data = project_data['extra_data']

        self.images = project_images

        self.gpt_client = assistant

    def funnel_flow(self):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += f"""
        Требуется сделать следующее:
        1) Привести воронку в цифрах в соответствии с имеющимися данными.
        2) Перечисли только 2 самых эффективных сценария на основе воронки, с помощью которых можно достигнуть цели: {self.metric_target}.
        К каждому сценарию напиши по одной проблемной гипотезе: почему эта метрика такая, а не больше."""

        messages = [
            {'role': 'system', 'content': prompts.FUNNEL_PROMPT},
            {'role': 'user', 'content': user_txt}
        ]

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens

    def ui_ux_flow(self):
        pass

    def save_to_md(self, report_data: str):
        with open('report', 'w+') as file:
            file.write(report_data)

    def start(self):
        answer, input_tokens, output_tokens = self.funnel_flow()
        self.save_to_md(answer)

