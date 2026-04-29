# presentation_repository
PPT Development in Github

## Streamlit PDF slideshow

This repository includes a Streamlit app that turns PDF pages into a slide show.

### Features

- Automatically finds PDF files in this repository directory.
- Lets you choose which PDF to present from the sidebar.
- Shows each PDF page as a slide.
- Provides Previous and Next buttons for slide navigation.
- Includes a slide number slider for jumping to any page.
- Includes Play and Pause controls for automatic slide playback.
- Lets you control the auto-play interval.
- Includes a render quality slider for sharper or faster PDF page rendering.

### Run the app

Run the app from this directory:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

### Use a new PDF

To use a different PDF in the app:

1. Add the new `.pdf` file to this repository directory.
2. Restart the Streamlit app if it is already running.
3. Open the app in your browser.
4. Select the new PDF from the sidebar dropdown.

The app lists every `.pdf` file placed directly inside this directory. If you replace an existing PDF with a newer version, keep the same file name or select the new file name from the sidebar.
