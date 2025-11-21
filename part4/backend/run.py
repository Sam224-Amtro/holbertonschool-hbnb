from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n=== Registered Routes ===")
    print("{:<45} {:<10}".format("Route", "Methods"))
    print("-" * 60)

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = ', '.join(sorted(m for m in rule.methods if m not in {'OPTIONS', 'HEAD'}))
        print("{:<45} {:<10}".format(rule.rule, methods))

    print("\nFrontend available at:")
    print(f"• http://localhost:5000/")
    print(f"• http://localhost:5000/login.html")
    print(f"• http://localhost:5000/place.html")
    print("\n=== Starting server ===")

    app.run(host='0.0.0.0', port=5000, debug=True)
