
class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        # lưu vị trí bị chiếu
        self.pins = []
        # kiểm tra vị trí bị chiếu
        self.checks = []
        # lưu vị trí Bắt Tốt qua đường
        self.enpassant_possible = ()
        # lưu lịch sử nước đi
        self.enpassant_possible_log = [self.enpassant_possible]
        #lưu trữ quyền động chốt của từng bên
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    # thực hiện một nước đi mới.
    def makeMove(self, move):
        # Xóa quân cờ từ ô xuất phát và di chuyển nó tới ô đích
        self.board[move.start_row][move.start_col] = "--"  # Xóa quân cờ từ ô xuất phát
        self.board[move.end_row][move.end_col] = move.piece_moved  # Di chuyển quân cờ tới ô đích

        # Thêm nước đi mới vào lịch sử di chuyển
        self.move_log.append(move)

        # Đảo ngược lượt chơi (từ trắng sang đen và ngược lại)
        self.white_to_move = not self.white_to_move

        # Nếu quân cờ di chuyển là vua, cập nhật vị trí vua
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        # Nếu đây là nước đi thăng cấp, thay thế quân tốt bằng hậu
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        # Nếu đây là nước đi en passant, loại bỏ quân tốt bị ăn
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"

        # Nếu quân cờ di chuyển là quân tốt và di chuyển 2 ô, thiết lập nước đi en passant tiềm năng
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        # Nếu đây là nước đi chốt, di chuyển quân chốt và vua
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # Di chuyển vua sang bên phải
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                    move.end_col + 1]  # Di chuyển quân chốt
                self.board[move.end_row][move.end_col + 1] = '--'  # Đặt ô trống tại vị trí cũ của quân chốt
            else:  # Di chuyển vua sang bên trái
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                    move.end_col - 2]  # Di chuyển quân chốt
                self.board[move.end_row][move.end_col - 2] = '--'  # Đặt ô trống tại vị trí cũ của quân chốt

        # Lưu lại nước đi en passant tiềm năng
        self.enpassant_possible_log.append(self.enpassant_possible)

        # Cập nhật quyền di chuyển chốt và lưu lại vào lịch sử
        self.updateCastleRights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs))
    # quay lại nước cũ
    def undoMove(self):
        # Kiểm tra xem có nước đi nào trong lịch sử không
        if len(self.move_log) != 0:
            # Lấy nước đi cuối cùng từ lịch sử di chuyển
            move = self.move_log.pop()
            # Đặt lại quân cờ từ ô đích về ô xuất phát
            self.board[move.start_row][move.start_col] = move.piece_moved
            # Đặt lại quân cờ đã bị ăn từ ô đích (nếu có)
            self.board[move.end_row][move.end_col] = move.piece_captured
            # Đảo ngược lượt chơi (từ đen sang trắng và ngược lại)
            self.white_to_move = not self.white_to_move

            # Nếu quân cờ di chuyển là vua, cập nhật lại vị trí vua
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # Nếu đây là nước đi en passant, loại bỏ quân tốt bị ăn và khôi phục nước đi en passant tiềm năng trước đó
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"  # Loại bỏ quân tốt bị ăn
                self.board[move.start_row][move.end_col] = move.piece_captured  # Khôi phục quân tốt bị ăn
            self.enpassant_possible_log.pop()  # Loại bỏ nước đi en passant tiềm năng cuối cùng
            self.enpassant_possible = self.enpassant_possible_log[-1]  # Khôi phục nước đi en passant tiềm năng trước đó

            # Loại bỏ quyền di chuyển chốt cuối cùng và khôi phục quyền di chuyển chốt trước đó
            self.castle_rights_log.pop()
            self.current_castling_rights = self.castle_rights_log[-1]

            # Nếu đây là nước đi chốt, di chuyển lại quân chốt và vua
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # Di chuyển vua sang bên phải
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                        move.end_col - 1]  # Di chuyển quân chốt
                    self.board[move.end_row][move.end_col - 1] = '--'  # Đặt ô trống tại vị trí cũ của quân chốt
                else:  # Di chuyển vua sang bên trái
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][
                        move.end_col + 1]  # Di chuyển quân chốt
                    self.board[move.end_row][move.end_col + 1] = '--'  # Đặt ô trống tại vị trí cũ của quân chốt

            # Đặt lại cờ kiểm tra checkmate và stalemate về False
            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        # Nếu có quân xe trắng bị ăn, vô hiệu hóa quyền castling tương ứng
        if move.piece_captured == "wR":
            if move.end_col == 0:
                self.current_castling_rights.wqs = False  # Không còn quyền castling bên trái cho trắng
            elif move.end_col == 7:
                self.current_castling_rights.wks = False  # Không còn quyền castling bên phải cho trắng
        # Nếu có quân xe đen bị ăn, vô hiệu hóa quyền castling tương ứng
        elif move.piece_captured == "bR":
            if move.end_col == 0:
                self.current_castling_rights.bqs = False  # Không còn quyền castling bên trái cho đen
            elif move.end_col == 7:
                self.current_castling_rights.bks = False  # Không còn quyền castling bên phải cho đen

        # Nếu vua trắng di chuyển, vô hiệu hóa tất cả quyền castling của trắng
        if move.piece_moved == 'wK':
            self.current_castling_rights.wqs = False
            self.current_castling_rights.wks = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bqs = False
            self.current_castling_rights.bks = False
        # Nếu có quân xe trắng di chuyển, vô hiệu hóa quyền castling tương ứng của trắng
        elif move.piece_moved == 'wR':
            if move.start_row == 7:  # Nếu quân xe di chuyển từ hàng 7 (vị trí ban đầu của quân xe trắng)
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False  # Không còn quyền castling bên trái cho trắng
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False  # Không còn quyền castling bên phải cho trắng
        # Nếu có quân xe đen di chuyển, vô hiệu hóa quyền castling tương ứng của đen
        elif move.piece_moved == 'bR':
            if move.start_row == 0:  # Nếu quân xe di chuyển từ hàng 0 (vị trí ban đầu của quân xe đen)
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False  # Không còn quyền castling bên trái cho đen
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False  # Không còn quyền castling bên phải cho đen

    def getValidMoves(self):
        # Lưu trữ quyền castling hiện tại để sau này phục hồi
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                          self.current_castling_rights.wqs, self.current_castling_rights.bqs)

        # Danh sách các nước đi hợp lệ
        moves = []

        # Kiểm tra xem có đang trong tình trạng chiếu
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        # Xác định vị trí của vua
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        # Nếu đang bị chiếu
        if self.in_check:
            if len(self.checks) == 1:  # Nếu chỉ có một quân chiếu
                moves = self.getAllPossibleMoves()

                # Tìm quân đang chiếu và vị trí của nó
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]

                # Tìm các ô hợp lệ để di chuyển vua
                valid_squares = []
                if piece_checking[1] == "N":  # Nếu quân đang chiếu là quân mã
                    valid_squares = [(check_row, check_col)]
                else:  # Nếu quân đang chiếu là quân khác
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                # Loại bỏ các nước đi không hợp lệ (không bảo vệ được vua)
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":  # Nếu nước đi không phải là di chuyển vua
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:  # Nếu có nhiều hơn một quân chiếu
                self.getKingMoves(king_row, king_col, moves)  # Chỉ di chuyển vua để thoát chiếu
        else:  # Nếu không bị chiếu
            moves = self.getAllPossibleMoves()  # Lấy tất cả các nước đi hợp lệ
            if self.white_to_move:
                self.getCastleMoves(self.white_king_location[0], self.white_king_location[1],
                                    moves)  # Kiểm tra castling cho vua trắng
            else:
                self.getCastleMoves(self.black_king_location[0], self.black_king_location[1],
                                    moves)  # Kiểm tra castling cho vua đen

        # Kiểm tra nếu không có nước đi nào thì kiểm tra checkmate hoặc stalemate
        if len(moves) == 0:
            if self.inCheck():  # Nếu vẫn đang trong tình trạng chiếu
                self.checkmate = True
            else:
                # TODO stalemate on repeated moves (Cần xác định stalemate khi di chuyển lặp lại)
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        # Phục hồi quyền castling ban đầu
        self.current_castling_rights = temp_castle_rights
        return moves

    def inCheck(self):
        # Kiểm tra nếu là lượt của người chơi trắng thì kiểm tra vị trí của vua trắng có bị chiếu hay không
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:  # Nếu là lượt của người chơi đen thì kiểm tra vị trí của vua đen có bị chiếu hay không
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

    def squareUnderAttack(self, row, col):
        # Tạm thời đổi lượt đi để lấy tất cả các nước đi có thể của đối phương
        self.white_to_move = not self.white_to_move
        opponents_moves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move

        # Kiểm tra xem ô có bị chiếu không bằng cách so sánh với các nước đi của đối phương
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  # Nếu ô này là một trong các ô mà đối phương có thể đi đến
                return True  # Trả về True, ô này bị chiếu
        return False  # Nếu không, trả về False, ô này không bị chiếu

    def getAllPossibleMoves(self):

        moves = []  # Khởi tạo một danh sách trống để lưu trữ các nước đi có thể

        # Duyệt qua tất cả các ô trên bàn cờ
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # Lấy màu của quân cờ trên ô hiện tại
                # Kiểm tra xem đến lượt của người chơi nào và quân cờ trên ô hiện tại có phải là của người chơi đó không
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]  # Lấy loại quân cờ trên ô hiện tại
                    # Gọi phương thức di chuyển tương ứng với loại quân cờ để lấy tất cả các nước đi có thể của quân cờ đó
                    self.moveFunctions[piece](row, col, moves)
        return moves  # Trả về danh sách các nước đi có thể của người chơi hiện tại

    def checkForPinsAndChecks(self):
        pins = []  # Danh sách các tình huống "pin"
        checks = []  # Danh sách các tình huống "check"
        in_check = False  # Biến để đánh dấu có đang bị chiếu không

        # Xác định màu quân cờ của đối phương và mình
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        # Các hướng có thể của quân cờ
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # Kiểm tra xem quân đối phương có thể chiếu hoặc chặn không
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():
                                # Nếu quân cờ đối phương có thể chiếu, đánh dấu là đang bị chiếu
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possible_pin)  # Nếu không, đánh dấu là tình huống "pin"
                                break
                        else:
                            break
                else:
                    break

        # Các nước đi của quân mã
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                # Kiểm tra xem quân mã đối phương có thể chiếu không
                if end_piece[0] == enemy_color and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))

        # Trả về kết quả sau khi kiểm tra
        return in_check, pins, checks

    def getPawnMoves(self, row, col, moves):

        piece_pinned = False  # Biến để xác định xem quân cờ có bị chặn không
        pin_direction = ()  # Hướng chặn nếu có
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])  # Lấy hướng chặn
                self.pins.remove(self.pins[i])
                break

        # Xác định hướng và mức độ di chuyển của quân tốt dựa trên màu và vị trí
        if self.white_to_move:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.black_king_location

        # Nếu ô trước tốt là trống, thì tốt có thể di chuyển về phía trước
        if self.board[row + move_amount][col] == "--":
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))
                if row == start_row and self.board[row + 2 * move_amount][
                    col] == "--":  # Nếu tốt ở vị trí ban đầu, nó có thể di chuyển 2 ô
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))

        # Nếu có quân địch ở chéo trái trước, tốt có thể tiến hành ăn quân đó
        if col - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move((row, col),
                                      (row + move_amount, col - 1), self.board))
                # Kiểm tra xem có thể di chuyển theo quy tắc "en passant" không
                if (row + move_amount, col - 1) == self.enpassant_possible:
                    # Kiểm tra xem việc di chuyển theo quy tắc "en passant" có thể tạo ra tình huống chiếu không
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    # Nếu không có quân tấn công hoặc có quân chặn, thì thêm nước đi "en passant" vào danh sách
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col),
                                          (row + move_amount, col - 1),
                                          self.board, is_enpassant_move=True))

        # Tương tự như trên, kiểm tra nước đi có thể ăn quân địch ở chéo phải trước đó
        if col + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move((row, col),
                                      (row + move_amount, col + 1), self.board))
                # Kiểm tra xem có thể di chuyển theo quy tắc "en passant" không
                if (row + move_amount, col + 1) == self.enpassant_possible:
                    # Kiểm tra xem việc di chuyển theo quy tắc "en passant" có thể tạo ra tình huống chiếu không
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    # Nếu không có quân tấn công hoặc có quân chặn, thì thêm nước đi "en passant" vào danh sách
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col),
                                          (row + move_amount, col + 1),
                                          self.board, is_enpassant_move=True))

    def getRookMoves(self, row, col, moves):

        piece_pinned = False  # Biến để xác định xem quân cờ có bị chặn không
        pin_direction = ()  # Hướng chặn nếu có
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])  # Lấy hướng chặn
                if self.board[row][col][1] != "Q":  # Nếu quân cờ không phải là quân hậu thì loại bỏ chặn
                    self.pins.remove(self.pins[i])
                break

        # Các hướng di chuyển của quân xe
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"  # Màu của quân địch
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Kiểm tra xem ô đích có nằm trong bàn cờ không
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                    -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Nếu ô đích trống
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # Ưu tiên ăn quân địch
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # Nếu gặp quân cờ đồng màu
                            break
                else:
                    break

    def getKnightMoves(self, row, col, moves):

        piece_pinned = False  # Biến để xác định xem quân cờ có bị chặn không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])  # Loại bỏ chặn nếu có
                break

        # Các nước đi của quân mã
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_color = "w" if self.white_to_move else "b"  # Màu của quân đồng minh
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Kiểm tra ô đích có nằm trong bàn cờ không
                if not piece_pinned:  # Nếu không bị chặn
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # Nếu ô đích không có quân đồng màu
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def getBishopMoves(self, row, col, moves):

        piece_pinned = False  # Biến để xác định xem quân cờ có bị chặn không
        pin_direction = ()  # Hướng của chặn nếu có
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])  # Loại bỏ chặn nếu có
                break

        # Các hướng di chuyển của quân tượng
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_color = "b" if self.white_to_move else "w"  # Màu của quân địch
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Kiểm tra ô đích có nằm trong bàn cờ không
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                    -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # Nếu ô đích trống
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # Nếu ô đích có quân địch
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, row, col, moves):

        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):

        # Các bước di chuyển của vua
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"  # Màu quân đang di chuyển
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Kiểm tra xem ô đích có nằm trong bàn cờ không
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Kiểm tra xem ô đích có phải quân địch không

                    # Lưu vị trí mới của vua tạm thời
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)

                    # Kiểm tra xem vua có bị chiếu không
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:  # Nếu vua không bị chiếu
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))  # Thêm nước đi vào danh sách hợp lệ

                    # Khôi phục vị trí ban đầu của vua
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def getCastleMoves(self, row, col, moves):

        # Kiểm tra xem ô hiện tại có bị chiếu không
        if self.squareUnderAttack(row, col):
            return

        # Kiểm tra xem có thể thực hiện phong cách tấn công vua không
        if (self.white_to_move and self.current_castling_rights.wks) or (
                not self.white_to_move and self.current_castling_rights.bks):
            self.getKingsideCastleMoves(row, col, moves)

        # Kiểm tra xem có thể thực hiện phong cách tấn công hậu không
        if (self.white_to_move and self.current_castling_rights.wqs) or (
                not self.white_to_move and self.current_castling_rights.bqs):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row, col, moves):
        # Kiểm tra xem các ô cần đi qua để thực hiện phong cách tấn công vua có trống không
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            # Kiểm tra xem các ô đi qua có bị chiếu không
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                # Thêm nước đi phong cách tấn công vua vào danh sách nước đi hợp lệ
                moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))

    def getQueensideCastleMoves(self, row, col, moves):
        # Kiểm tra xem các ô cần đi qua để thực hiện phong cách tấn công hậu có trống không
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            # Kiểm tra xem các ô đi qua có bị chiếu không
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                # Thêm nước đi phong cách tấn công hậu vào danh sách nước đi hợp lệ
                moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        # Khởi tạo đối tượng CastleRights với quyền được phép castling cho từng bên
        self.wks = wks  # Quyền castling của trắng ở cánh vua (King's side)
        self.bks = bks  # Quyền castling của đen ở cánh vua (King's side)
        self.wqs = wqs  # Quyền castling của trắng ở cánh hậu (Queen's side)
        self.bqs = bqs  # Quyền castling của đen ở cánh hậu (Queen's side)

class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        # Khởi tạo một nước đi mới
        self.start_row = start_square[0]  # Hàng bắt đầu của quân cờ
        self.start_col = start_square[1]  # Cột bắt đầu của quân cờ
        self.end_row = end_square[0]  # Hàng kết thúc của quân cờ
        self.end_col = end_square[1]  # Cột kết thúc của quân cờ
        self.piece_moved = board[self.start_row][self.start_col]  # Quân cờ đã di chuyển
        self.piece_captured = board[self.end_row][self.end_col]  # Quân cờ bị bắt (nếu có)

        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                self.piece_moved == "bp" and self.end_row == 7)  # Kiểm tra xem có phải là quân bãi tốt không
        self.is_enpassant_move = is_enpassant_move  # Kiểm tra xem có phải là nước đi en passant không
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"  # Xác định quân cờ bị bắt ở nước đi en passant

        self.is_castle_move = is_castle_move  # Kiểm tra xem có phải là nước đi castling không

        self.is_capture = self.piece_captured != "--"  # Kiểm tra xem có phải là nước đi bắt quân cờ không
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col  # ID của nước đi

    def __eq__(self, other):
        # So sánh hai nước đi
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # Trả về biểu diễn của nước đi theo chuẩn notation của cờ vua
        if self.is_pawn_promotion:
            return self.getRankFile(self.end_row, self.end_col) + "Q"
        if self.is_castle_move:
            if self.end_col == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.is_enpassant_move:
            return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                self.end_col) + " e.p."
        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.start_row, self.start_col)[0] + "x" + self.getRankFile(self.end_row,
                                                                                                    self.end_col)
            else:
                return self.piece_moved[1] + "x" + self.getRankFile(self.end_row, self.end_col)
        else:
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.getRankFile(self.end_row, self.end_col)

    def getRankFile(self, row, col):
        # Chuyển đổi hàng và cột thành Rank và File tương ứng
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self):
        # Trả về biểu diễn chuỗi của nước đi
        if self.is_castle_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.getRankFile(self.end_row, self.end_col)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square
