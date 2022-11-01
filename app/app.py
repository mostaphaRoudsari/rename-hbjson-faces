import streamlit as st
from honeybee.model import Model
import json
from pollination_streamlit_io import get_hbjson

st.header('Rename room faces based on room name and orientation')
st.write(
    'This app takes an HBJSON file and rename the display name for faces based on '
    'the room display name and the orientation of the face. You can download the new '
    'version of the file.'
)
model = get_hbjson(key='my-model')
if model:
    model = Model.from_dict(model['hbjson'])
    for room in model.rooms:
        st.write(f'Rename faces for: {room.display_name}')
        room_name = room.display_name
        for face in room.faces:
            try:
                face_dir = face.horizontal_orientation()
            except ZeroDivisionError:
                face.display_name = f'{room_name}..{face.type}'
            else:
                if 0 <= face_dir < 45 or 270 + 45 <= face_dir:
                    face_dir = 'N'
                elif 45 <= face_dir < 90 + 45:
                    face_dir = 'E'
                elif 90 + 45 <= face_dir < 180 + 45:
                    face_dir = 'S'
                else:
                    face_dir = 'W'
                face.display_name = f'{room_name}..{face_dir}'
            for count, aperture in enumerate(face.apertures):
                aperture.display_name = f'{face.display_name}..{count}'
            for count, door in enumerate(face.doors):
                door.display_name = f'{face.display_name}..{count}'

    st.download_button(
        'Download updated HBJSON file',
        data=json.dumps(model.to_dict()),
        file_name=f'{model.display_name}.hbjson'
    )
