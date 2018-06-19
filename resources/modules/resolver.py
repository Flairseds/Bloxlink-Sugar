from discord.utils import find

def string_resolver(message, arg, content=None):
	if not content:
		content = message.content

	min = arg.get("min", -100)
	max = arg.get("max", 100)

	if arg.get("min") or arg.get("max"):
		if min <= len(content) <= max:
			return str(content), None
		else:
			return False, f'String character count not in range: {min}-{max}'

	return str(content), None

def number_resolver(message, arg, content=None):
	if not content:
		content = message.content

	if content.isdigit():
		min = arg.get("min", -100)
		max = arg.get("max", 100)

		if arg.get("min") or arg.get("max"):
			if min <= len(content) <= max:
				return int(content), None
			else:
				return False, f'Number character count not in range: {min}-{max}'
		else:
			return int(content), None

		return int(content), None

	return False, "You must pass a number"

def choice_resolver(message, arg, content=None):
	if not content:
		content = message.content

	for choice in arg["choices"]:
		if choice.lower() == content.lower():
			return choice, None

	return False, f'Choice must be of either: {str(arg["choices"])}'

def user_resolver(message, arg, content=None):
	if not content:
		content = message.content

	guild = message.guild

	if message.mentions:
		return message.mentions[0], None
	else:
		is_int, is_id = None, None

		try:
			is_int = int(content)
			is_id = is_int > 15
		except ValueError:
			pass

		if is_id:
			return guild.get_member(is_int), None
		else:
			return guild.get_member_named(content), None

	return False, "Invalid user"

def channel_resolver(message, arg, content=None):
	if not content:
		content = message.content

	guild = message.guild

	if message.channel_mentions:
		return message.channel_mentions[0], None
	else:
		is_int, is_id = None, None

		try:
			is_int = int(content)
			is_id = is_int > 15
		except ValueError:
			pass

		if is_id:
			return guild.get_channel(is_int), None
		else:
			return find(lambda c: c.name == content, guild.text_channels), None

	return False, "Invalid channel"

def role_resolver(message, arg, content=None):
	if not content:
		content = message.content

	guild = message.guild

	if message.role_mentions:
		return message.role_mentions[0], None
	else:
		is_int, is_id = None, None

		try:
			is_int = int(content)
			is_id = is_int > 15
		except ValueError:
			pass

		if is_id:
			return find(lambda r: r.id == is_int, guild.roles), None
		else:
			return find(lambda r: r.name == content, guild.roles), None

	return False, "Invalid role"

resolver_map = {
	"string": string_resolver,
	"number": number_resolver,
	"choice": choice_resolver,
	"user": user_resolver,
	"channel": channel_resolver,
	"role": role_resolver,
}