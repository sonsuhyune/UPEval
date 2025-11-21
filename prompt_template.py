import os
from jinja2 import Template


class PromptTemplate:
    def __init__(self, prompt_type):
        if "upeval" in prompt_type :
            template_path = "prompts/gen.jinja"
        else:
            raise ValueError("prompt type is not valid.")

        with open(template_path, 'r') as fp:
            self.template = Template(fp.read())
        self.prompt = self.template.blocks['prompt']
        # empty_context = self.template.new_context()
    
    def prompting(self, **kwargs):
        context = self.template.new_context(kwargs)
        return ''.join(self.prompt(context)).strip()

    def checker_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['checker']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def scoring_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['scoring']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def repeat_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['repeat']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def repeat_score_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['repeat_score']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def repeat_score_only_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['repeat_score_only']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def cot_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['cot']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()

    def supporter_prompting(self, **kwargs):
        supporter_prompt = self.template.blocks['supporter']
        context = self.template.new_context(kwargs)
        return ''.join(supporter_prompt(context)).strip()

    def neg_prompting(self, **kwargs):
        cot_prompt = self.template.blocks['convert_neg']
        context = self.template.new_context(kwargs)
        return ''.join(cot_prompt(context)).strip()



if __name__ == '__main__':
    # template_path = './prompts/gen.jinja'
    prompt_type = "vanilla"
