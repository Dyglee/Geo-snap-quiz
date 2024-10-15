from app import create_app

print("Creating app...")
app = create_app()
print("App created successfully")

if __name__ == '__main__':
    print("Running app locally...")
    app.run(debug=True)