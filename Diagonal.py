    def get_successors(self, playing_for):
		"""	Get the successor from the current state based on player.		"""
		successor_list = []
		for row in range(len(self.board)):
			for column in range(len(self.board[row])):
				if (self.board[row][column] == 0):
					indexrow = row
					indexcolumn = column

					newboard = copy.deepcopy(self.board)

					newboard[row][column] = playing_for
                    decision = remove_successors(self,newboard,indexrow,indexcolumn,playing_for)
                    if(decision == 1):
					    newstate = State(newboard, "min")
					    successor_list.append(newstate)
		return successor_list

    def remove_successors(self,newstate,indexrow,indexcolumn,playing_for):
        boarddimensions = len(self.board)
        boarddimensions = boarddimensions **(0.5)
        column = 0
        score_row = 0
        decision = 1
        for b in range(0,boarddimensions):
            if (newstate[indexrow][column] == playing_for):
                score_row += 1
            column += 1
        if(score_row == boarddimensions)
            decision = 0

        score_column = 0
        row = 0
        for b in range(0, boarddimensions):
            if (newstate[row][indexcolumn] == playing_for):
                score_column += 1
            row += 1

        if(score_column == boarddimensions):
            decision = 0

        x = indexrow
        y = indexcolumn
        counter = 0
        scoreofdiagonal = 0
        while (x > -1 and y < boarddimensions):
            if (newstate[x][y] == playing_for):
                scoreofdiagonal += 1
            x = x - 1
            y += 1
            counter += 1

        if(scoreofdiagonal == counter):
            decision = 0

        x = indexrow
        y = indexcolumn
        counter = 0
        scoreofdiagonal = 0
        while (x < boarddimensions and y < boarddimensions):
            if (newstate[x][y] == playing_for):
                scoreofdiagonal += 1
            x += 1
            y += 1
            counter += 1

        if (scoreofdiagonal == counter):
            decision = 0

        x = indexrow
        y = indexcolumn
        counter = 0
        scoreofdiagonal = 0
        while (x > -1 and y > -1):
            if (newstate[x][y] == playing_for):
                scoreofdiagonal += 1
            x = x - 1
            y = y - 1
            counter += 1

        if (scoreofdiagonal == counter):
            decision = 0

        x = indexrow
        y = indexcolumn
        counter = 0
        scoreofdiagonal = 0
        while (x < boarddimensions and y > -1):
            if (newstate[x][y] == playing_for):
                scoreofdiagonal += 1
            x += 1
            y = y -1
            counter += 1

        if (scoreofdiagonal == counter):
            decision = 0

        return decision



