'''
Given a string, we want to express the following values as:

whitespace: [' ', '\t', '\n']
digits: ['0' - '9']
numbers: [digits ... digits] (set of sequential digits)
letters: ['a'-'z', 'A'-'Z']
ids: [letters ... letters] (set of sequential letters)
keywords: ids in tk_ids, which are found in the token defintions when concated

other values, are add-ons to the intial set, i.e operators etc

sequentials are a result of combined digits/letters
'''

#single-token defintions for values with same token keys
tk_def = {
    "white": [' ', '\t', '\n'],
    "digit": [chr(i) for i in range(48, 58)],
    "letter": [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
}

'''
Token Ids for any keywords to add-on

THIS IS WHAT YOU EDIT TO ADD TYPES TO INTERPRETER, i.e abs(x), let x=5 in x+1.
                                                       keyw    keyw   keyw
'''
tk_ids = [
    "abs",
    "let",
    "in"
]

class Token:
    def __init__(self):
        pass

    def sep_string(str):
        return list(enumerate((str)))

    def in_(val, ls):
        return val in ls

    '''
    Reads in a string-rep of a token, and returns a token, with {TYPE: input}

    i.e: "a" -> {LETTER: a}, "+" -> {PLUS: +}
    '''
    def eval_token(str_token, offset=0):
        match str_token:
            case v if Token.in_(v, tk_def["white"]): return {"WHITE": str_token}
            case v if Token.in_(v, tk_def["digit"]): return {"DIGIT": str_token}
            case v if Token.in_(v, tk_def["letter"]): return {"LETTER": str_token}
            case "+": return {"PLUS": str_token}
            case "-": return {"MINUS": str_token}
            case "*": return {"MULT": str_token}
            case "/": return {"DIV": str_token}
            case "(": return {"LBRAC": str_token}
            case ")": return {"RBRAC": str_token}
            case "=": return {"EQUAL": str_token}
            case _:
                raise Exception(f"Lexer Error: Invalid string-rep token found at offset {offset}: <{str_token}>")

    '''
    Takes the current token being analyzed, and the next token, then updates its accordingly

    i.e: {DIGIT: 1}, {DIGIT: 2} -> {NUMBER: 12}

    note, all single digits/letters (non-sequential) get converted to their non-sequential form
    '''
    def concat_eval_token(cur_token, token):
        match (cur_token, token):
            case ({"DIGIT": cv}, {"DIGIT": tv}) | ({"NUMBER": cv}, {"DIGIT": tv}):
                return {"NUMBER": cv+tv}
            case (_, {"DIGIT": tv}):
                return {"NUMBER": tv}

            case ({"LETTER": cv}, {"LETTER": tv}) | ({"ID": cv}, {"LETTER": tv}):
                return {"ID": cv+tv}
            case (_,{"LETTER": tv}):
                return {"ID": tv}

            case _:
                return token
    '''
    Converts string into a list of single char tokens

    Errors if an invalid token is found, treating it as the index in the string where there is an invalid token
    '''
    def gen_tk_list(str):
        return [Token.eval_token(i, indx) for indx, i in Token.sep_string(str)]
            
    def concat_tokens(tk_list):
        ls = [{"WHITE": ' '}] + tk_list + [{"WHITE": ' '}]
        conc_list = []
        for i in range(1, len(ls)-1):

            tk = Token.concat_eval_token(tk, ls[i]) if i>1 else Token.concat_eval_token(ls[i-1], ls[i])
            
            #pushes to array of array if same token as new token, else makes new array of array
            if(i > 1 and list(conc_list[-1][0].keys())[0] == list(tk.keys())[0]):
                conc_list[-1] += [tk]
            else:
                conc_list += [[tk]]

        return conc_list

    def rm_interm_tokens(tk_list):
        res = []
        for i in tk_list:
            match i:
                case [{"NUMBER": _}, *t] | [{"ID": _}, *t]:
                    res += [i[-1]]
                case [{"WHITE": _}, *t]:
                    pass
                case _:
                    res += [x for x in i]
        return res

    '''
    Converts any ids to a key if found in tk_ids
    '''
    def get_keywords(tk_list):
        for indx, i in enumerate(tk_list):
            match i:

                #convert id -> key if found
                case {"ID": id} if id.lower() in tk_ids:
                    tk_list[indx] = {"KEY": id.lower()}
                
                #convert number form str -> int
                case {"NUMBER": num}:
                    tk_list[indx] = {"NUMBER": int(num)}
                case _:
                    pass
        return tk_list
                

    '''
    Converts a string fully to a list of tokens that can be used in the CST

    (final product of lexer)
    '''
    def parse_string(str):
        return Token.get_keywords(Token.rm_interm_tokens(Token.concat_tokens(Token.gen_tk_list(str))))