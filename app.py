import gradio as gr
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


#https://www.youtube.com/watch?v=bhR274lZNLo
def get_transcript(video_url):
    video_id=video_url.split("v=")[1].split("&")[0]
    #return video_id    
    transcript=YouTubeTranscriptApi.get_transcript(video_id,languages=['en','tr'])
    raw_text=" ".join([entry['text'] for entry in transcript])
    return raw_text
#print (get_transcript("https://www.youtube.com/watch?v=bhR274lZNLo"))
def fn_sum_text(transkript_text, word_count, model_sel, lang_sel, action_sel,GEMINI_API_KEY):
    client=genai.Client(api_key=GEMINI_API_KEY)
    prompt=f"{transkript_text} metni {word_count} sayıda kelimeyle {lang_sel} dilinde {action_sel}"
    response=client.models.generate_content(
    model=model_sel,
    contents=[prompt]
)
    return (response.text)
#video_url='https://www.youtube.com/watch?v=bhR274lZNLo'
with gr.Blocks(theme= gr.themes.Citrus()) as demo:
    gr.Markdown("## Youtube Video Url Çeviri-Özet Gemini API")
    with gr.Row():
        with gr.Column():
            video_url=gr.Textbox(placeholder="Youtube Video URL")
            trs_btn=gr.Button('Transkripti Al')
            GEMINI_API_KEY=gr.Textbox(placeholder="GEMINI API KEY", type="password" , show_label=False)
            word_count=gr.Slider(minimum=50,
            maximum=1000,
            value=200,
            step=10 , label = "Kelime Sayısı Seçimi")
            model_sel=gr.Dropdown(
                choices=['gemini-2.0-flash',
                'gemini-2.0-flash-lite',
                'gemini-1.5-pro'],
                value='gemini-2.0-flash',
                label="Model Seçimi"
            )
            lang_sel=gr.Dropdown(
                choices=['Türkçe',
                'İngilizce',
                'Almanca' , 
                'Rusça' , 
                'İspanyolca'],
                value='Türkçe',
                label="Dil Seçimi"
            )
            action_sel=gr.Dropdown(
                choices=['Özetle',
                'Tam çeviri yap.'],
                value='Özetle',
                label="İşlem"
            )
            sum_btn=gr.Button('Özetle')
        with gr.Column():
            transkript_text=gr.Textbox(label='Transkripti', lines=5)
            sum_text=gr.Textbox(label='Özet', lines=5)
        trs_btn.click(fn=get_transcript,
        inputs=video_url,
        outputs=transkript_text
        )
        sum_btn.click(fn=fn_sum_text,
        inputs=[transkript_text, word_count, model_sel, lang_sel, action_sel,GEMINI_API_KEY],
        outputs=sum_text
        )

demo.launch()
        

if _name=='main_':
    demo.launch()