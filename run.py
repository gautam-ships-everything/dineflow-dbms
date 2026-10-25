from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 65)
    print(" DineFlow: Intelligent Restaurant Management & DBMS Project")
    print(" Developed by: Gautam Soni (Enrollment: 0808CS241120)")
    print(" Department of Computer Science & Engineering, IPS Academy")
    print(" Server starting on: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(host='127.0.0.1', port=5000, debug=True)
