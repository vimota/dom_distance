# Ordered set recipe taken from http://code.activestate.com/recipes/576694/
import collections

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

#######################################
import re
from sets import Set

DOM_PATTERN = '([0-9a-zA-z-_]+)(#[0-9a-zA-z-_]*)?(\.[0-9a-zA-z-_.]*)?'

class DomElement:
	def __init__(self, tag, tag_id, classes):
		self.tag = tag
		self.id = tag_id
		self.classes = OrderedSet(classes)

	def __str__(self):
		# adds '.' before each class name and joins them
		classes_string = ''.join(map(lambda x: ".{0}".format(x), self.classes))

		formatted = self.tag
		if self.id:
			formatted+= "#" + self.id
		formatted += classes_string

		return formatted
		#return "DomElement({0}, {1}, {2})".format(self.tag, self.id, self.classes)

	def __repr__(self):
		return str(self)

	def copy(self):
		return DomElement(self.tag, self.id, list(self.classes))


def parse_dom(dom_string):
	dom = []
	for element in dom_string.split(' '):
		m = re.match(DOM_PATTERN, element)

		tag = m.group(1)
		tag_id = (m.group(2)[1:] if m.group(2) else None)
		classes = (m.group(3).split('.')[1:] if m.group(3) else [])

		dom_element = DomElement(tag, tag_id, classes)
		dom.append(dom_element)

	return dom


def shortest_distance(original, target):
	# print original
	# print target

	if str(original) == str(target):
		# base case
		return 0

	o_len = len(original)
	t_len = len(target)
	distances = []
	for i in range(max(o_len, t_len)):
		if o_len != t_len and i == min(o_len, t_len):

			# Case where everything has been correct until the end of
			# either original or target
			if i == t_len:
				# We must delete the remainder of the original
				cost = o_len - t_len
				original = original[0:i]


			else:
				# i == o_len
				# We must add the remaining elements to original
				cost = 0
				for element in target[i:]:
					original.append(element.copy())
					cost += 1
					if element.id:
						cost += 1
					cost += len(element.classes)

			return cost

		elif str(original[i]) == str(target[i]):
			continue

		else:
			current_o = original[i]
			current_t = target[i]

			# Follow path that alters current node to look like target node

			alter_cost = 0
			if current_o.tag != current_t.tag:
				alter_cost += 1
			if current_o.id != current_t.id:
				if not current_t.id or not current_o.id:
					# have to remove or add new id
					alter_cost += 1
				else:
					# have to remove current id and add new id
					alter_cost += 2
			if current_o.classes != current_t.classes:
				alter_cost += len(current_o.classes | current_t.classes) - len(current_o.classes & current_t.classes)

			altered_dom = original[0:i] + [current_t.copy()] + original[i+1:]

			try:
				distances.append(shortest_distance(altered_dom, target) + alter_cost)
			except Exception, e:
				raise Exception(str(altered_dom))


			# Follow path that deletes current node

			delete_cost = 1
			deleted_dom = original[0:i] + original[i+1:]
			distances.append(shortest_distance(deleted_dom, target) + delete_cost)

			# Follow path that adds new node

			add_cost = 1
			if current_t.id:
				# cost of adding id
				add_cost += 1
			#cost of adding classes
			add_cost += len(current_t.classes)

			added_dom = original[0:i] + [current_t.copy()] + original[i:]
			distances.append(shortest_distance(added_dom, target) + add_cost)

			return min(distances)


with open('test_cases.txt') as f:
		original = f.readline().rstrip('\n')

		while (original != ''):
			target = f.readline().rstrip('\n')
			distance = f.readline().rstrip('\n')


			original_dom = parse_dom(original)
			target_dom = parse_dom(target)
			print shortest_distance(original_dom, target_dom)

			break
			original = f.readline().rstrip('\n')
