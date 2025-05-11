
from app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        # Debug=True enables debug mode, but we disable the built-in debugger and reloader
        # to work better with external debuggers
        app.run(debug=True, use_debugger=False, use_reloader=False)
    except Exception as e:
        print(f"Error: {e}")
