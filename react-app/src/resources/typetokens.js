export class TypeToken {
    constructor(value, privilege) {
        this.value = value; 
        this.privilege = privilege; 
    }
}

export class NumberTypeToken extends TypeToken {}
export class VariableTypeToken extends TypeToken {}

export class SymbolTypeToken extends TypeToken {
    constructor (value, label, privilege) {
        super(value, privilege); 
        this.value = value; 
        this.label = label; 
        this.privilege = privilege; 
    }
}