import streamlit as st
from honeybee.model import Model
from pollination_streamlit_io import get_hbjson, send_hbjson

st.header('Rename room faces based on room name and orientation')
st.info(
    'This app takes a Pollination model and rename the display name for faces based on '
    'the room display name and the orientation of the face.'
)

model = get_hbjson(
    key='get-po-model', label='Get Pollination Model',
    options={'selection': {'selected': True}}
)

if model:
    model: Model = Model.from_dict(model['hbjson'])
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

    st.success(
        'The model faces are re-named. Use this button to either add the current model '
        'to Rhino or replace the model in Rhino with the new model.'
    )
    send_hbjson(
        key='send-po-model',
        hbjson=model.to_dict(),
        option='replace',
        options={
            'preview': False, 'clear': False, 'subscribe-preview': False
        }
    )
