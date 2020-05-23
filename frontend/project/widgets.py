import streamlit as st

def bubble(labels, values, colors):

    return f"""
<style>
.bubble {{
    position: absolute;
    display: flex;
    border-radius: 9999px; 
    align-items: center;
    justify-content: center;
    color: white;
    text-align: center;
}}
.bubble-text {{
        line-height: 18px;
}}
</style>
<div style="position: relative; width: 200px; height: 250px;">
    <div 
    class="bubble"
    style="
    top: 0;
    left: 0;
    background-color: {colors[0]}; 
    width:150px; 
    height: 150px;
    "
    >
    {labels[0]}</br>{values[0]}
    </div>
    <div 
    class="bubble bubble-text"
    style="
    top: 73px;
    left: 172px;
    background-color: {colors[1]}; 
    width: 80px; 
    height: 80px;
    "
    >
    {labels[1]}</br>{values[1]}
    </div>
    <div
    class="bubble bubble-text"
    style="
    top: 162px;
    left: 26px;
    background-color: {colors[2]}; 
    width: 85px; 
    height: 85px;
    "
    >
    {labels[2]}</br>{values[2]}
    </div>
    <div 
    class="bubble bubble-text"
    style="
    top: 151px;
    left: 118px;
    background-color: {colors[3]}; 
    width: 60px; 
    height: 60px;
    "
    >
    {labels[3]}</br>{values[3]}
    </div>
</div>
"""

def tiles(title, titleValue, subTitles, subValues):


    return f"""
<div>
    <div style="
    width: auto; 
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #d7dadf;
    margin: 10px;
    text-align: center;      
    box-sizing: border-box;
    ">
        {title} </br> {titleValue}
    </div>
    <div style="
    width: 100%;
    display: flex;
    ">
        <div style="
        width: 33%;
        height: 100px;
        display: flex;
        align-items: center;
        text-align: center;      
        justify-content: center;
        background-color: #bbd0ff;
        margin: 10px;
        ">
        {subTitles[0]} </br> {subValues[0]}
        </div>
        <div style="
        width: 33%;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center; 
        text-align: center;      
        background-color: #bbd0ff;
        margin: 10px;
        ">
        {subTitles[1]} </br> {subValues[1]}
        </div>
        <div style="
        width: 33%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;      
        height: 100px;
        background-color: #bbd0ff;
        margin: 10px;
        ">
        {subTitles[2]} </br> {subValues[2]}
        </div>
    </div>
</div>
"""


def video_youtube(src: str, width="100%", height=315):
    """An extension of the video widget
    Arguments:
        src {str} -- A youtube url like https://www.youtube.com/embed/B2iAodr0fOo
    Keyword Arguments:
        width {str} -- The width of the video (default: {"100%"})
        height {int} -- The height of the video (default: {315})
    """
    st.write(
        f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        unsafe_allow_html=True,
    )