import chess
import chess.engine
import numpy
import keras.models as models




MyModel = models.load_model('model.h5')

indexSquares = {
  'a': 0, 'b': 1,'c': 2,'d': 3,'e': 4,'f': 5,'g': 6,'h': 7
}

def SquareToIndex(mySquare):
  letter = chess.square_name(mySquare)
  return 8 - int(letter[1]), indexSquares[letter[0]]

def splitDimension(board):
  threedboard = numpy.zeros((14, 8, 8), dtype=numpy.int8)

  for p in chess.PIECE_TYPES:
    for square in board.pieces(p, chess.WHITE):
      idx = numpy.unravel_index(square, (8, 8))
      threedboard[p - 1][7 - idx[0]][idx[1]] = 1
    for square in board.pieces(p, chess.BLACK):
      idx = numpy.unravel_index(square, (8, 8))
      threedboard[p + 5][7 - idx[0]][idx[1]] = 1

  myturn = board.turn
  board.turn = chess.WHITE
  for move in board.legal_moves:
      i, j = SquareToIndex(move.to_square)
      threedboard[12][i][j] = 1
  board.turn = chess.BLACK
  for move in board.legal_moves:
      i, j = SquareToIndex(move.to_square)
      threedboard[13][i][j] = 1
  board.turn = myturn

  return threedboard


def MinimaxEval(board):
  threedboard = splitDimension(board)
  threedboard = numpy.expand_dims(threedboard, 0)
  return MyModel.predict(threedboard)[0][0]


def Minimax(board, depth, alpha, beta, maximizingPlayer):
  if depth == 0 or board.is_game_over():
    return MinimaxEval(board)
  
  if maximizingPlayer:
    maxEval = -numpy.inf
    for move in board.legal_moves:
      board.push(move)
      eval = MinimaxEval(board)
      board.pop()
      maxEval = max(maxEval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return maxEval
  else:
    minEval = numpy.inf
    for move in board.legal_moves:
      board.push(move)
      eval = MinimaxEval(board)
      board.pop()
      minEval = min(minEval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return minEval



def GetAiMove(board, depth):
  maxMove = None
  maxEval = -numpy.inf

  for move in board.legal_moves:
    board.push(move)
    eval = Minimax(board, depth - 1, -numpy.inf, numpy.inf, False)
    board.pop()
    if eval > maxEval:
      maxEval = eval
      maxMove = move
  
  return maxMove



