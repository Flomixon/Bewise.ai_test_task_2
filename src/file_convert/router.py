import os
import uuid
import shutil
from pydub import AudioSegment

from fastapi import (
    APIRouter, Depends, File, HTTPException, Path, Request, UploadFile
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.base_config import current_user
from file_convert.models import Song
from database import get_async_session


file_convert_router = APIRouter()


@file_convert_router.post('/convert')
async def convert(
    request: Request,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(
        description="Загрузить аудиофайл в формате '.wav'"
    )
):
    '''Эндпоинт для преобразования аудиофайла из '.wav' в '.mp3' '''
    if file.content_type == 'audio/wav':
        name_bd = file.filename.replace('.wav', '.mp3')
        id = uuid.uuid4()
        save_name = f'media/{user.id}/{id}.mp3'
        with open(f'{id}.wav', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        try:
            song = AudioSegment.from_wav(f'{id}.wav')
            song.export(save_name, format='mp3')
        except:
            return HTTPException(
                status_code=422,
                detail='Неверная кодировка файла'
            )
        finally:
            os.remove(f'{id}.wav')
        song = Song(id=id, user_created=user.id, name=name_bd)
        session.add(song)
        await session.commit()
        return f'{request.base_url}record?id={id}&user={user.id}'
    return HTTPException(
        status_code=422,
        detail="Аудиофайл должен иметь расширение '.wav'"
    )


@file_convert_router.get('/record')
async def download(
    id: str = Path(description="id аудиозаписи"),
    user: int = Path(description="id пользователя добавившего запись"),
    session: AsyncSession = Depends(get_async_session)
):
    '''Эндпоинт для загрузки преобразованного аудиофайла в '.mp3' '''
    filename = await session.get(Song, id)
    return FileResponse(f'media/{user}/{id}.mp3', filename=filename.name)
