from flask import Flask, render_template, request, jsonify
from solver import solve_sudoku, generate_sudoku

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    grid = data.get('grid')
    if not grid:
        return jsonify({"error": "No grid provided"}), 400
    
    solved_grid = solve_sudoku(grid)
    
    if solved_grid:
        return jsonify({
            "solved": True,
            "grid": solved_grid
        })
    else:
        return jsonify({
            "solved": False,
            "message": "No solution exists"
        })

@app.route('/api/generate', methods=['GET'])
def generate():
    difficulty = request.args.get('difficulty', 'medium')
    puzzle = generate_sudoku(difficulty=difficulty)
    return jsonify({"grid": puzzle})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
