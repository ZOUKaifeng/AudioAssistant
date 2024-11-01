import asyncio
import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from interface import pipeline  # 引入你的 inference pipeline
from io import BytesIO
import soundfile as sf
import base64
import numpy as np
import json


# def pipeline(audio):
#     return {"speech": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
#             "response": "0", 
#             "transcript": "0"}

app = FastAPI()
sample_rate=16000
@app.websocket("/TranscribeStreaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_open = True
    stop_audio_stream = False  
    audio_queue = asyncio.Queue()  # 用于存储从前端接收到的音频数据

    async def mic_stream():
        while not stop_audio_stream:
            indata = await audio_queue.get()
            yield indata, None

    async def write_chunks():
        sample_rate=16000
        async for chunk, _ in mic_stream():
            try:
                # 使用 pipeline 处理音频数据并返回AI生成的回答
                results = pipeline(audio=chunk)
                if results["response"] != "0":
                    with BytesIO() as buffer:
                        sf.write(buffer, results["speech"], samplerate=16000, format='WAV')
                        buffer.seek(0)
                        # 将字节数据进行 base64 编码
                        encoded_audio = base64.b64encode(buffer.read()).decode('utf-8')
                else:
                    encoded_audio = base64.b64encode(results["speech"]).decode('utf-8')
            
                response = json.dumps({
                        "event": 'audio_processed',
                        "user":results["transcript"],
                        "text_response": results["response"],
                        "synthesized_audio_data": encoded_audio
                    })
                

                # 通过 WebSocket 发送音频数据
                await websocket.send(({"type": "websocket.send", "text": response}))
                print("data sent")              
                
                
                
            except OSError as e:
                logging.error(f"OSError: {e}")
                break

    try:
        send_task = asyncio.create_task(write_chunks())

        while websocket_open:
            message = await websocket.receive()
            
            if message["type"] == "websocket.receive":
                if "bytes" in message:
                    audio_chunk = message["bytes"]
                    logging.info(f"Received binary data: {audio_chunk[:10]}... (truncated)")
                    # 将音频数据放入队列
                    await audio_queue.put(audio_chunk)
                elif "text" in message:
                    text_message = message["text"]
                    
               
                    
                    logging.info(f"Received message: {text_message}")
                    

                    try:
                        message_data = json.loads(text_message)
                      
                        
                        if message_data.get("event") == "process_audio":
                            audio_data = message_data.get("audio_data")
                            if audio_data:
                                # 将Base64编码的音频数据解码为字节
                                audio_bytes = base64.b64decode(audio_data)
                                print(f"Decoded audio data: {audio_bytes[:10]}... (truncated)")
                                logging.info(f"Decoded audio data: {audio_bytes[:10]}... (truncated)")
                                # 将音频数据放入队列
                                await audio_queue.put(audio_bytes)

                    except OSError as e:
                        logging.error(f"OSError: {e}")
                        break

                    if text_message == "submit_response":
                        # 前端请求停止音频流并获取结果
                        stop_audio_stream = True
                        await send_task  # 等待音频流处理完成
                        break

    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    finally:
        websocket_open = False
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, ws_ping_interval=None)
