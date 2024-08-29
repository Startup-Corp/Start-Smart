from assistent import Assistent
from objects.gpt_requests import AddRequest
from objects.project import UploadReport
import prompts as prompts
import base64
import logging


FLOW_STATUS = {
    'funnel': 0,
    'uiux': 1,
    'competitors': 2,
    'hypotzy': 3,
    'roadmap': 4
}

class GPTFlow:
    def __init__(self, project_data: dict, project_images: list, assistant: Assistent, bucket_id: str, project_id: int, is_dev: bool = False):
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

        self.bucket_id = bucket_id
        self.project_id = project_id
        self.result = None

        self.is_dev = is_dev

    def funnel_flow(self):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}
        Описание воронки: {self.funnel_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += f"""
        Требуется сделать следующее:
        1) Привести воронку в цифрах в соответствии с имеющимися данными.
        2) Перечисли только 2 самых эффективных сценария на основе воронки, с помощью которых можно достигнуть цели: {self.metric_target}.
        К каждому сценарию напиши по одной проблемной гипотезе: почему эта метрика такая, а не больше."""

        prompt = prompts.TMP_PRODUCT_PROMPT if self.is_dev else prompts.PRODUCT_PROMPT
        user_txt = 'Ты aboba' if self.is_dev else user_txt

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_txt}
        ]

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens
    
    def ui_ux_flow(self):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}
        Описание скриншотов: {self.img_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += """
        Требуется сделать следующее:
        1) Провести Анализ дизайна по интерфейсам.
        2) Предложи 3 проблемные гипотезы и способы решения."""

        prompt = prompts.TMP_UI_UX_PROMPT if self.is_dev else prompts.UI_UX_PROMPT
        user_txt = 'Ты aboba' if self.is_dev else user_txt

        messages = [
            {'role': 'system', 'content': prompt},
            {
                'role': 'user', 
                'content': [
                    {
                        'type': 'text',
                        'text': user_txt
                    }
                ]
            }
        ]

        if self.is_dev is False:
            for image in self.images:
                image_base64 = base64.b64encode(image)
                messages[1]['content'].append({'type': 'image_url', 'image_url':{'url': f'data:image/jpeg;base64,{image_base64.decode()}'}})

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens

    def competitors_flow(self):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += """
        Создай качественный анализ конкурентов для рассматриваемого продукта. 
        Включи информацию о возможных конкурентах, включая банки, финансовые платформы и интернет-платформы, 
        их рыночные позиции, стратегии маркетинга и ключевые особенности их предложений."""

        prompt = prompts.TMP_PRODUCT_PROMPT if self.is_dev else prompts.PRODUCT_PROMPT
        user_txt = 'Ты aboba' if self.is_dev else user_txt

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_txt}
        ]

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens
    
    def hypotzy_flow(self, funnel_answer: str, ui_ux_answer: str):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}
        Описание воронки: {self.funnel_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += f"Ниже представлен анализ воронки\n\n{funnel_answer}"
        user_txt += f"Ниже представлен анализ интерфейса\n\n{ui_ux_answer}"

        user_txt += """
        Требуется сделать следующее:
        1) На основе имеющихся данных сформулируй 5 гипотез в формате User Story.
        2) Выбери 5 метрик для подсчета приоритета гипотезы.
        3) Посчитай каждую метрику для каждой гипотезы и выстави приоритеты. Ответ на этот пункт предоставь в виде таблицы.
        4) Выбери одну единственную гипотезу, которую следует исследовать и объясни почему."""

        prompt = prompts.TMP_PRODUCT_PROMPT if self.is_dev else prompts.PRODUCT_PROMPT
        user_txt = 'Ты aboba' if self.is_dev else user_txt

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_txt}
        ]

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens
    
    def roadmap_flow(self, hypotzy_answer):
        user_txt = f"""
        Описание проекта: {self.description}
        Цель: {self.metric_target}
        Название метрики: {self.metric_title}
        Описание метрики: {self.metric_desc}
        Описание воронки: {self.funnel_desc}"""

        if self.extra_data:
            user_txt += f"Так же известна дополнительная информация: {self.extra_data}"

        user_txt += f"Ниже представлен список гипотез и их анализ, а так же выбор наилучшей\n\n{hypotzy_answer}"

        user_txt += """
        Требуется сделать следующее:
        1) Распиши Roadmap того, как проверить наилучшую гипотезу по шагам.
        2) Уточни на что стоит обратить внимание при проверке."""

        prompt = prompts.TMP_PRODUCT_PROMPT if self.is_dev else prompts.PRODUCT_PROMPT
        user_txt = 'Ты aboba' if self.is_dev else user_txt

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_txt}
        ]

        answer, input_tokens, output_tokens = self.gpt_client.create_request(messages)
        return answer, input_tokens, output_tokens

    def save_to_md(self, report_data: str):
        logging.info(f'GPT Flow. pr_id: {self.project_id}. Save Data')
        self.result = report_data
        if self.is_dev:
            with open('report.md', 'w') as file:
                file.write(report_data)
        UploadReport.execute(self.bucket_id, self.project_id, report_data.encode())

    def get_result(self) -> bytes:
        if self.result is None:
            return b'aboba'
        return str.encode(self.result)

    def start(self):
        total_answer = ''

        logging.info(f'GPT Flow. pr_id: {self.project_id}. Run Funnel flow')
        funnel_answer, input_tokens, output_tokens = self.funnel_flow()
        total_answer += funnel_answer
        AddRequest.execute(self.project_id, input_tokens, output_tokens, funnel_answer, FLOW_STATUS['funnel'])

        logging.info(f'GPT Flow. pr_id: {self.project_id}. Run UI UX flow')
        uiux_answer, input_tokens, output_tokens = self.ui_ux_flow()
        total_answer += uiux_answer
        AddRequest.execute(self.project_id, input_tokens, output_tokens, uiux_answer, FLOW_STATUS['uiux'])

        logging.info(f'GPT Flow. pr_id: {self.project_id}. Run Competitors flow')
        competitors_answer, input_tokens, output_tokens = self.competitors_flow()
        total_answer += competitors_answer
        AddRequest.execute(self.project_id, input_tokens, output_tokens, competitors_answer, FLOW_STATUS['competitors'])

        logging.info(f'GPT Flow. pr_id: {self.project_id}. Run Hypotzy flow')
        hypotzy_answer, input_tokens, output_tokens = self.hypotzy_flow(funnel_answer, uiux_answer)
        total_answer += hypotzy_answer
        AddRequest.execute(self.project_id, input_tokens, output_tokens, hypotzy_answer, FLOW_STATUS['hypotzy'])

        logging.info(f'GPT Flow. pr_id: {self.project_id}. Run Roadmap flow')
        roadmap_answer, input_tokens, output_tokens = self.roadmap_flow(hypotzy_answer)
        total_answer += roadmap_answer
        AddRequest.execute(self.project_id, input_tokens, output_tokens, roadmap_answer, FLOW_STATUS['roadmap'])

        self.save_to_md(total_answer)

