export class Token { }

export class NumberToken extends Token {
    constructor (value) {
        super(); 
        this.value = value; 
    }
}

export class VariableToken extends Token {
    constructor (value) {
        super(); 
        this.value = value; 
    }
}

export class PointerToken extends Token {
    constructor (point) {
        super(); 
        this.point = point; 
    }

    fetch_destination () {
        return this.point; 
    }
}

export class BracketsToken extends Token {
    constructor (start, content, end) {
        super(); 
        this.start = start; 
        this.content = content; 
        this.end = end; 
        this.privilege = 5; 
    }
}

export class OperatorToken extends Token {
    constructor (left, right, privilege, label) {
        super(); 
        this.left = left; 
        this.right = right; 
        
        this.privilege = privilege; 
        this.label = label; 
    }
}