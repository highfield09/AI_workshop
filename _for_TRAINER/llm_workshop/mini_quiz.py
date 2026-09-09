"""Short end-of-workbook practice quizzes; no external calls or saved answers."""
from html import escape
import ipywidgets as widgets
from llm_workshop.quiz import _message

# question, choices, correct index, explanation
QUESTIONS = {
    '01_start_here': [
        ('Which README welcomes you to the whole workshop?', ['README.md at the repository root', '_for_STUDENT/data/notebook1/README.md', 'Any file with README in its name'], 0, 'The full path matters. Root README.md describes the whole project; nested READMEs explain their own folders.'),
        ('How do you run a notebook cell?', ['Rename its file', 'Shift + Enter or the play button', 'Close the notebook'], 1, 'Running a code cell produces its output or widget. After a kernel restart, rerun setup and the activity.'),
        ('Which prompt gives an AI the clearest target?', ['Make something good', 'Do everything', 'Name the input, desired output and constraints'], 2, 'A concrete target and relevant context give you something specific to check and refine.'),
        ('An AI returns a confident factual answer. What next?', ['Accept confidence as proof', 'Open its sources and check the claim', 'Ask it to sound more certain'], 1, 'Ask for citations when needed and check that the original sources actually support the answer.'),
    ],
    '02_models_and_reasoning': [
        ('What helps you choose a model that can interpret images?', ['Its name alone', 'Its modality labels and model card', 'The longest description'], 1, 'Check supported input types and capability icons. Not every language model accepts images.'),
        ('How should you compare two models fairly?', ['Use the same prompt and compare the results', 'Change the task for each model', 'Judge only the response length'], 0, 'Keeping the prompt fixed makes differences easier to interpret; longer answers are not automatically better.'),
        ('Which rule is best when choosing model size?', ['Always choose the largest', 'Always choose the smallest', 'Balance task quality, cost and resources'], 2, 'Size alone does not guarantee the best result for your specific task.'),
        ('Good scientific reasoning guarantees a correct EC identifier. True?', ['Yes, reasoning guarantees recall', 'No—verify the identifier in an authoritative database', 'Only if the answer is long'], 1, 'Reasoning and precise knowledge retrieval are different abilities. Check classifications and identifiers independently.'),
    ],
    '03_vision_and_context': [
        ('Before asking about an image, what should you confirm?', ['An image attachment chip is present', 'Its filename is short', 'The image is mentioned somewhere on disk'], 0, 'A file path in text is not proof that the model received the image. Attach it and inspect the response.'),
        ('Why can a short follow-up still have many input tokens?', ['Input tokens measure only your new sentence', 'Only answers use tokens', 'Earlier messages and attachments may be included'], 2, 'Chat context can include previous turns, tool results and attachments; provider processing and caching also affect usage.'),
        ('You are switching to a different project. What is a useful habit?', ['Keep adding unrelated instructions', 'Start a new focused chat', 'Assume unlimited memory'], 1, 'The active context is bounded. Older material may be summarised or omitted, and unrelated context can reduce relevance.'),
        ('Where do you inspect input/output tokens and cost for your OpenRouter-key request?', ['Only the GitHub repository page', 'OpenRouter Activity', 'The image properties dialog'], 1, 'Check the service handling your request. The editor and the billing provider are not always the same.'),
    ],
    '04_debugging': [
        ('A NameError says disco_colours is undefined. What should you inspect?', ['Variable spelling and where it was defined', 'The invoice CSV', 'Your display brightness'], 0, 'Compare the reported name with the code that creates it; a small spelling mismatch can stop execution.'),
        ('Which debugging prompt keeps the repair focused?', ['Rewrite the entire project', 'Ignore the traceback', 'Explain this error and give the smallest fix'], 2, 'Include the relevant code and traceback. Ask for a small change you can understand and test.'),
        ('The AI suggests a repair. How do you know it worked?', ['The answer sounds confident', 'Apply it, rerun, and inspect the result', 'Delete the error message'], 1, 'A proposed fix is a hypothesis until the code runs and the intended behaviour is checked.'),
        ('Agent mode has edited your notebook. What should you do?', ['Accept every change without checking', 'Review the scoped edit and rerun the cell', 'Assume automatic edits are always correct'], 1, 'Agent mode can change files and use tools. You still review what changed and verify the intended result.'),
    ],
    '06_receipt_ocr': [
        ('Full-page OCR finishes normally. What does that prove?', ['Every printed detail was captured', 'The output still needs comparison with the image', 'The reference CSV is unnecessary for any check'], 1, 'A completed response can still omit a field or misread a value. Preserve raw text and inspect the source.'),
        ('In this decimal-comma example, what quantity does 3,00 mean?', ['300', '0.03', '3'], 2, 'The comma is a decimal separator. Do not remove it blindly; write an actual numeric Excel cell.'),
        ('Where should a receipt grand total be stored?', ['Once per receipt, separate from item rows', 'As the price of every item', 'As an item quantity'], 0, 'Define what one row represents. Repeating invoice totals across item rows causes double-counting.'),
        ('Before charting the 20-receipt batch, what matters?', ['Silently discard failures', 'Count rows instead of quantities', 'Audit failures and use checked numeric quantities'], 2, 'Account for every input, exclude unresolved rows explicitly, and explain grouping and unit choices. The first 20 files are not a representative sales sample.'),
    ],
}


def mini_quiz(workbook):
    items = QUESTIONS[workbook]
    number = int(workbook[:2])
    cards = []
    for index, (prompt, options, _, _) in enumerate(items, 1):
        title = widgets.HTML(_message(f'<b>W{number} · MINI QUIZ {index}</b><br>{escape(prompt)}', 'info'))
        choices = widgets.RadioButtons(options=[(label, i) for i, label in enumerate(options)], value=None,
            layout=widgets.Layout(width='100%', min_width='0', min_height='110px', overflow='visible'))
        feedback = widgets.HTML(_message('Choose one answer.', 'info'))
        cards.append(widgets.VBox([title, choices, feedback], layout=widgets.Layout(
            width='100%', min_width='0', padding='10px', margin='0 0 12px 0', border='1px solid #B2DDFF')))
    submit = widgets.Button(description='Submit quiz', icon='check', button_style='primary')
    summary = widgets.HTML(_message('Answer all four questions, then submit. You can try again.', 'info'))
    def check(_):
        correct = unanswered = 0
        for card, (_, options, answer, explanation) in zip(cards, items):
            selected = card.children[1].value
            if selected is None:
                unanswered += 1
                card.children[2].value = _message('Choose an answer, then submit again.', 'warning')
            else:
                ok = selected == answer
                correct += int(ok)
                text = '<b>Correct!</b> ' if ok else f'<b>Not quite.</b> Correct answer: <b>{escape(options[answer])}</b>. '
                card.children[2].value = _message(text + escape(explanation), 'success' if ok else 'error')
        summary.value = _message(f'<b>{correct}/4 correct.</b> {unanswered} unanswered. Review the explanations and try again if helpful.', 'success' if correct == 4 else 'info')
    def changed(change):
        for card in cards:
            if card.children[1] is change['owner']:
                card.children[2].value = _message('Answer selected or changed; submit to check it.', 'info')
        summary.value = _message('Submit to check your current choices.', 'info')
    for card in cards:
        card.children[1].observe(changed, names='value')
    submit.on_click(check)
    style = widgets.HTML("<style>.mini-quiz .widget-radio-box label {white-space:normal!important;height:auto!important;line-height:1.5;margin:5px 0;align-items:flex-start}.mini-quiz .widget-radio-box {width:100%;min-width:0}</style>")
    box = widgets.VBox([style, *cards, submit, summary], layout=widgets.Layout(width='100%', max_width='100%', min_width='0'))
    box.add_class('workshop-widget')
    box.add_class('mini-quiz')
    return box
