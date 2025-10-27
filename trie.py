class TrieNode:
    def __init__(self, char=''):
        self.char = char
        self.is_end = False
        self.children = {}
        self.counter = 0

class Trie:
    def __init__(self):
        self.root = TrieNode("")
    
    def insert(self, word):
        """Inserta una palabra en el Trie"""
        node = self.root
        word = word.lower()
        
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        node.is_end = True
    
    def dfs(self, node, prefix):
        """Búsqueda en profundidad para encontrar todas las palabras"""
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
    
    def search(self, prefix):
        """Busca todas las palabras que empiezan con el prefijo"""
        node = self.root
        prefix = prefix.lower()
        
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        
        self.output = []
        self.dfs(node, prefix[:-1] if prefix else "")
        
        self.output.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in self.output[:10]]
    
    def increment_counter(self, word):
        """Incrementa el contador cuando se selecciona una palabra"""
        node = self.root
        word = word.lower()
        
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return
        
        if node.is_end:
            node.counter += 1
    
    def get_stats(self):
        """Obtiene estadísticas del Trie"""
        words = []
        self._collect_words(self.root, "", words)
        words.sort(key=lambda x: -x[1])
        return words[:10]
    
    def _collect_words(self, node, prefix, words):
        """Recolecta todas las palabras con sus contadores"""
        if node.is_end:
            words.append((prefix, node.counter))
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, words)
