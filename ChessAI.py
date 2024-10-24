import random
# Bảng điểm cố định của từng quân cờ
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
# Bảng điểm vị trí cho quân mã
knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]
# Bảng điểm vị trí cho quân tịnh
bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
# Tạo từ điển lưu trữ điểm vị trí cho mỗi loại quân cờ và màu sắc

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],# Đảo ngược điểm của quân mã cho màu đen
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}
# Hằng số cho điểm checkmate và stalemate
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Độ sâu tìm kiếm cho thuật toán minimax


# Hàm tìm nước đi tốt nhất sử dụng negamax với cắt alpha-beta
def findBestMove(game_state, valid_moves, return_queue):
    global next_move  # Biến để lưu trữ nước đi tốt nhất
    next_move = None  # Khởi tạo next_move
    random.shuffle(valid_moves)  # Trộn danh sách các nước đi hợp lệ để tạo ngẫu nhiên
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)  # Gọi thuật toán negamax
    return_queue.put(next_move)  # Đưa nước đi tốt nhất vào hàng đợi trả về

# Hàm đệ quy cho negamax với cắt alpha-beta
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move  # Biến để lưu trữ nước đi tốt nhất
    if depth == 0:  # Trường hợp cơ sở: đạt đến độ sâu tối đa
        return turn_multiplier * scoreBoard(game_state)  # Trả về điểm đánh giá
    max_score = -CHECKMATE  # Khởi tạo điểm cao nhất
    for move in valid_moves:  # Lặp qua các nước đi hợp lệ
        game_state.makeMove(move)  # Thực hiện nước đi
        next_moves = game_state.getValidMoves()  # Lấy các nước đi hợp lệ cho lượt kế tiếp
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)  # Gọi đệ quy
        if score > max_score:  # Cập nhật điểm cao nhất nếu cần
            max_score = score
            if depth == DEPTH:
                next_move = move  # Lưu nước đi tốt nhất nếu ở mức gốc
        game_state.undoMove()  # Hoàn tác nước đi
        if max_score > alpha:  # Cập nhật alpha nếu cần
            alpha = max_score
        if alpha >= beta:  # Thực hiện cắt alpha-beta
            break
    return max_score

# Hàm để đánh giá trạng thái hiện tại của trò chơi
def scoreBoard(game_state):
    if game_state.checkmate:  # Nếu trò chơi kết thúc bằng checkmate
        if game_state.white_to_move:
            return -CHECKMATE  # Trả về điểm thấp cho chiến thắng của quân đen
        else:
            return CHECKMATE  # Trả về điểm cao cho chiến thắng của quân trắng
    elif game_state.stalemate:  # Nếu trò chơi kết thúc bằng stalemate
        return STALEMATE  # Trả về điểm 0
    score = 0  # Khởi tạo điểm
    for row in range(len(game_state.board)):  # Lặp qua các hàng
        for col in range(len(game_state.board[row])):  # Lặp qua các cột
            piece = game_state.board[row][col]  # Lấy quân cờ tại vị trí hiện tại
            if piece != "--":  # Nếu vị trí không trống
                piece_position_score = 0  # Khởi tạo điểm vị trí
                if piece[1] != "K":  # Loại trừ vua khỏi điểm vị trí
                    piece_position_score = piece_position_scores[piece][row][col]  # Lấy điểm vị trí từ bảng tra cứu
                if piece[0] == "w":  # Nếu quân thuộc về quân trắng
                    score += piece_score[piece[1]] + piece_position_score  # Cộng điểm quân cờ và điểm vị trí
                if piece[0] == "b":  # Nếu quân thuộc về quân đen
                    score -= piece_score[piece[1]] + piece_position_score  # Trừ điểm quân cờ và điểm vị trí
    return score  # Trả về điểm cuối cùng

# Hàm để tìm một nước đi ngẫu nhiên nếu đã đạt đến độ sâu tìm kiếm
def findRandomMove(valid_moves):
    return random.choice(valid_moves)  # Trả về một nước đi ngẫu nhiên từ danh sách các nước đi hợp lệ