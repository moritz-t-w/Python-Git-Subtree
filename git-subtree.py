import subprocess


class GitSubtree:
	"""
	Subtrees allow subprojects to be included within a subdirectory of the
	main project, optionally including the subproject’s entire history.

	For example, you could include the source code for a library as a
	subdirectory of your application.

	Subtrees are not to be confused with submodules, which are meant for
	the same task. Unlike submodules, subtrees do not need any special
	constructions (like .gitmodules files or gitlinks) be present in your
	repository, and do not force end-users of your repository to do
	anything special or to understand how subtrees work. A subtree is just
	a subdirectory that can be committed to, branched, and merged along
	with your project in any way you want.

	They are also not to be confused with using the subtree merge strategy.
	The main difference is that, besides merging the other project as a
	subdirectory, you can also extract the entire history of a subdirectory
	from your project and make it into a standalone project. Unlike the
	subtree merge strategy you can alternate back and forth between these
	two operations. If the standalone library gets updated, you can
	automatically merge the changes into your project; if you update the
	library inside your project, you can "split" the changes back out again
	and merge them back into the library project.

	For example, if a library you made for one application ends up being
	useful elsewhere, you can extract its entire history and publish that
	as its own git repository, without accidentally intermingling the
	history of your application project.

		Tip

		In order to keep your commit messages clean, we recommend that
		people split their commits between the subtrees and the main
		project as much as possible. That is, if you make a change that
		affects both the library and the main application, commit it in two
		pieces. That way, when you split the library commits out later,
		their descriptions will still make sense. But if this isn’t
		important to you, it’s not necessary. git subtree will simply leave
		out the non-library-related parts of the commit when it splits it
		out into the subproject later.

	Original `git-subtree` documentation written by Avery Pennarun
	apenwarr@gmail.com, adapted for python by Moritz T. W.
	`git-subtree` is a part of the `git` suite.
	"""

	def __init__(
		self,
		repository_path: str,
		command: str = "git subtree",
		prefix: str = None,
		quiet: bool = False,
		debug: bool = False
	):
		"""
		:param repository_path:
			Path to an existing git repository.
		:param command:
			Command to pass the generated git-subtree args to.
		:param prefix:
			Specify the path in the repository to the subtree you want to
			manipulate. This option is mandatory for all commands.
		:param quiet:
			Suppress unnecessary output messages on stderr.
			Produce even more unnecessary output messages on stderr.
		"""
		self.repository_path = repository_path
		self.command = command
		self.prefix = prefix
		self.quiet = quiet
		self.debug = debug

	def add(self, local_commit: str, squash: bool = False, message: str = None):
		"""
		Create the `prefix` subtree by importing its contents from the
		given `local_commit`. A new commit is created automatically,
		joining the imported project’s history with your own.

		:param squash:
			Import only a single commit from the subproject,
			rather than its entire history.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

		:param message:
			Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"add",
			{
				"squash": squash,
				"m": message
			},
			local_commit
		)

	def add(self, repository: str, remote_ref: str, squash: bool = False, message: str = None):
		"""
		Create the `prefix` subtree by importing its contents from the
		`repository` and `remote_ref`. A new commit is created
		automatically, joining the imported project’s history with your own.

		:param squash:
			Import only a single commit from the subproject,
			rather than its entire history.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

		:param message:
			Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"add",
			{
				"squash": squash,
				"m": message
			},
			repository,
			remote_ref
		)

	def merge(self, local_commit: str, repository: str = None, squash: bool = False, message: str = None):
		"""
		Merge recent changes up to `local_commit` into the `prefix`
		subtree. As with normal git merge, this doesn’t remove your own
		local changes; it just merges those changes into the latest
		`local_commit`.

		:param squash:
			Create only one commit that contains
			all the changes, rather than merging in the entire history.
			If you use `squash`, the merge direction doesn’t always have to be
			forward; you can use this command to go back in time from v2.5 to
			v2.4, for example. If your merge introduces a conflict, you can
			resolve it in the usual ways.
			When using `squash`, and the previous merge with `squash` merged an
			annotated tag of the subtree repository, that tag needs to be
			available locally. If `repository` is given, a missing tag will
			automatically be fetched from that repository.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

		:param message:
			Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"merge",
			{
				"squash": squash,
				"m": message
			},
			local_commit,
			repository
		)

	def split(
		self,
		local_commit: str = None,
		repository: str = None,
		annotate: str = None,
		branch: str = None,
		ignore_joins: bool = False,
		onto: str = None,
	):
		"""
		Extract a new, synthetic project history from the history of the
		`prefix` subtree of `local_commit`, or of HEAD if no `local_commit`
		is given. The new history includes only the commits (including
		merges) that affected `prefix`, and each of those commits now has
		the contents of `prefix` at the root of the project instead of in a
		subdirectory. Thus, the newly created history is suitable for
		export as a separate git repository.

		After splitting successfully, a single commit ID is printed to
		stdout. This corresponds to the HEAD of the newly created tree,
		which you can manipulate however you want.

		Repeated splits of exactly the same history are guaranteed to be
		identical (i.e. to produce the same commit IDs) as long as the
		settings passed to split (such as `annotate`) are the same. Because
		of this, if you add new commits and then re_split, the new commits
		will be attached as commits on top of the history you generated
		last time, so git merge and friends will work as expected.

		When a previous merge with `squash` merged an annotated tag of the
		subtree repository, that tag needs to be available locally. If
		`repository` is given, a missing tag will automatically be fetched
		from that repository.

		:param annotate:
			When generating synthetic history, add `annotation` as a prefix to
			each commit message. Since we’re creating new commits with the same
			commit message, but possibly different content, from the original
			commits, this can help to differentiate them and avoid confusion.
			Whenever you split, you need to use the same `annotation`, or else
			you don’t have a guarantee that the new re_created history will be
			identical to the old one. That will prevent merging from working
			correctly. git subtree tries to make it work anyway, particularly
			if you use `rejoin`, but it may not always be effective.

		:param branch:
			After generating the synthetic history, create a new branch called
			`branch` that contains the new history. This is suitable for
			immediate pushing upstream. `branch` must not already exist.

		:param ignore_joins:
			If you use `rejoin`, git subtree attempts to optimize its history
			reconstruction to generate only the new commits since the last
			`rejoin`.  `ignore_joins` disables this behavior, forcing it to
			regenerate the entire history. In a large project, this can take a
			long time.

		:param onto:
			If your subtree was originally imported using something other than
			git subtree, its history may not match what git subtree is
			expecting. In that case, you can specify the commit ID `onto` that
			corresponds to the first revision of the subproject’s history that
			was imported into your project, and git subtree will attempt to
			build its history from there.
			If you used git subtree add, you should never need this option.
		"""
		self.__run(
			"split",
			{
				"annotate": annotate,
				"b": branch,
				"ignore-joins": ignore_joins,
				"onto": onto
			},
			local_commit,
			repository
		)

	def split(
		self,
		local_commit: str = None,
		repository: str = None,
		annotate: str = None,
		branch: str = None,
		ignore_joins: bool = False,
		onto: str = None,
		rejoin: bool = False,
		message: str = None,
		squash: bool = False
	):
		"""
		Extract a new, synthetic project history from the history of the
		`prefix` subtree of `local_commit`, or of HEAD if no `local_commit`
		is given. The new history includes only the commits (including
		merges) that affected `prefix`, and each of those commits now has
		the contents of `prefix` at the root of the project instead of in a
		subdirectory. Thus, the newly created history is suitable for
		export as a separate git repository.

		After splitting successfully, a single commit ID is printed to
		stdout. This corresponds to the HEAD of the newly created tree,
		which you can manipulate however you want.

		Repeated splits of exactly the same history are guaranteed to be
		identical (i.e. to produce the same commit IDs) as long as the
		settings passed to split (such as `annotate`) are the same. Because
		of this, if you add new commits and then re_split, the new commits
		will be attached as commits on top of the history you generated
		last time, so git merge and friends will work as expected.

		When a previous merge with `squash` merged an annotated tag of the
		subtree repository, that tag needs to be available locally. If
		`repository` is given, a missing tag will automatically be fetched
		from that repository.

		:param annotate:
			When generating synthetic history, add `annotation` as a prefix to
			each commit message. Since we’re creating new commits with the same
			commit message, but possibly different content, from the original
			commits, this can help to differentiate them and avoid confusion.
			Whenever you split, you need to use the same `annotation`, or else
			you don’t have a guarantee that the new re_created history will be
			identical to the old one. That will prevent merging from working
			correctly. git subtree tries to make it work anyway, particularly
			if you use `rejoin`, but it may not always be effective.

		:param branch:
			After generating the synthetic history, create a new branch called
			`branch` that contains the new history. This is suitable for
			immediate pushing upstream. `branch` must not already exist.

		:param ignore_joins:
			If you use `rejoin`, git subtree attempts to optimize its history
			reconstruction to generate only the new commits since the last
			`rejoin`.  `ignore_joins` disables this behavior, forcing it to
			regenerate the entire history. In a large project, this can take a
			long time.

		:param onto:
			If your subtree was originally imported using something other than
			git subtree, its history may not match what git subtree is
			expecting. In that case, you can specify the commit ID `onto` that
			corresponds to the first revision of the subproject’s history that
			was imported into your project, and git subtree will attempt to
			build its history from there.
			If you used git subtree add, you should never need this option.

		:param rejoin:
			After splitting, merge the newly created synthetic history back
			into your main project. That way, future splits can search only the
			part of history that has been added since the most recent `rejoin`.
			If your split commits end up merged into the upstream subproject,
			and then you want to get the latest upstream version, this will
			allow git’s merge algorithm to more intelligently avoid conflicts
			(since it knows these synthetic commits are already part of the
			upstream repository).
			Unfortunately, using this option results in git log showing an
			extra copy of every new commit that was created (the original, and
			the synthetic one).
			If you do all your merges with `squash`, make sure you also use
			`squash` when you split `rejoin`.

		:param squash:
			Create only one commit that contains
			all the changes, rather than merging in the entire history.
			If you use `squash`, the merge direction doesn’t always have to be
			forward; you can use this command to go back in time from v2.5 to
			v2.4, for example. If your merge introduces a conflict, you can
			resolve it in the usual ways.
			When using `squash`, and the previous merge with `squash` merged an
			annotated tag of the subtree repository, that tag needs to be
			available locally. If `repository` is given, a missing tag will
			automatically be fetched from that repository.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

		:param message:
			Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"split",
			{
				"annotate": annotate,
				"b": branch,
				"ignore-joins": ignore_joins,
				"onto": onto,
				"rejoin": rejoin,
				"squash": squash,
				"m": message
			},
			local_commit,
			repository
		)

	def pull(self, repository: str, remote_ref: str, message: str = None, squash: bool = False):
		"""
		Exactly like merge, but parallels git pull in that it fetches the
		given ref from the specified remote repository.

		:param squash:
			Create only one commit that contains
			all the changes, rather than merging in the entire history.
			If you use `squash`, the merge direction doesn’t always have to be
			forward; you can use this command to go back in time from v2.5 to
			v2.4, for example. If your merge introduces a conflict, you can
			resolve it in the usual ways.
			When using `squash`, and the previous merge with `squash` merged an
			annotated tag of the subtree repository, that tag needs to be
			available locally. If `repository` is given, a missing tag will
			automatically be fetched from that repository.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

		:param message:
			Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"pull",
			{
				"m": message,
				"squash": squash
			},
			repository,
			remote_ref
		)

	def push(
		self,
		repository: str,
		local_commit: str = None,
		remote_ref: str = None,
		annotate: str = None,
		branch: str = None,
		ignore_joins: bool = False,
		onto: str = None,
	):
		"""
		Does a split using the `prefix` subtree of `local_commit` and then
		does a git push to push the result to the `repository` and
		`remote_ref`. This can be used to push your subtree to different
		branches of the remote repository. Just as with split, if no
		`local_commit` is given, then HEAD is used.

		:param annotate:
			When generating synthetic history, add `annotation` as a prefix to
			each commit message. Since we’re creating new commits with the same
			commit message, but possibly different content, from the original
			commits, this can help to differentiate them and avoid confusion.
			Whenever you split, you need to use the same `annotation`, or else
			you don’t have a guarantee that the new re_created history will be
			identical to the old one. That will prevent merging from working
			correctly. git subtree tries to make it work anyway, particularly
			if you use `rejoin`, but it may not always be effective.

		:param branch:
			After generating the synthetic history, create a new branch called
			`branch` that contains the new history. This is suitable for
			immediate pushing upstream. `branch` must not already exist.

		:param ignore_joins:
			If you use `rejoin`, git subtree attempts to optimize its history
			reconstruction to generate only the new commits since the last
			`rejoin`.  `ignore_joins` disables this behavior, forcing it to
			regenerate the entire history. In a large project, this can take a
			long time.

		:param onto:
			If your subtree was originally imported using something other than
			git subtree, its history may not match what git subtree is
			expecting. In that case, you can specify the commit ID `onto` that
			corresponds to the first revision of the subproject’s history that
			was imported into your project, and git subtree will attempt to
			build its history from there.
			If you used git subtree add, you should never need this option.
		"""
		self.__run(
			"push",
			{
				"annotate": annotate,
				"b": branch,
				"ignore-joins": ignore_joins,
				"onto": onto
			},
			repository,
			local_commit,
			remote_ref
		)

	def push(
		self,
		repository: str,
		local_commit: str = None,
		remote_ref: str = None,
		annotate: str = None,
		branch: str = None,
		ignore_joins: bool = False,
		onto: str = None,
		rejoin: bool = False,
		squash: bool = False,
		message: str = None
	):
		"""
		Does a split using the `prefix` subtree of `local_commit` and then
		does a git push to push the result to the `repository` and
		`remote_ref`. This can be used to push your subtree to different
		branches of the remote repository. Just as with split, if no
		`local_commit` is given, then HEAD is used.

		:param annotate:
			When generating synthetic history, add `annotation` as a prefix to
			each commit message. Since we’re creating new commits with the same
			commit message, but possibly different content, from the original
			commits, this can help to differentiate them and avoid confusion.
			Whenever you split, you need to use the same `annotation`, or else
			you don’t have a guarantee that the new re_created history will be
			identical to the old one. That will prevent merging from working
			correctly. git subtree tries to make it work anyway, particularly
			if you use `rejoin`, but it may not always be effective.

		:param branch:
			After generating the synthetic history, create a new branch called
			`branch` that contains the new history. This is suitable for
			immediate pushing upstream. `branch` must not already exist.

		:param ignore_joins:
			If you use `rejoin`, git subtree attempts to optimize its history
			reconstruction to generate only the new commits since the last
			`rejoin`.  `ignore_joins` disables this behavior, forcing it to
			regenerate the entire history. In a large project, this can take a
			long time.

		:param onto:
			If your subtree was originally imported using something other than
			git subtree, its history may not match what git subtree is
			expecting. In that case, you can specify the commit ID `onto` that
			corresponds to the first revision of the subproject’s history that
			was imported into your project, and git subtree will attempt to
			build its history from there.
			If you used git subtree add, you should never need this option.

		:param rejoin:
			After splitting, merge the newly created synthetic history back
			into your main project. That way, future splits can search only the
			part of history that has been added since the most recent `rejoin`.
			If your split commits end up merged into the upstream subproject,
			and then you want to get the latest upstream version, this will
			allow git’s merge algorithm to more intelligently avoid conflicts
			(since it knows these synthetic commits are already part of the
			upstream repository).
			Unfortunately, using this option results in git log showing an
			extra copy of every new commit that was created (the original, and
			the synthetic one).
			If you do all your merges with `squash`, make sure you also use
			`squash` when you split `rejoin`.

		:param squash:
			Create only one commit that contains
			all the changes, rather than merging in the entire history.
			If you use `squash`, the merge direction doesn’t always have to be
			forward; you can use this command to go back in time from v2.5 to
			v2.4, for example. If your merge introduces a conflict, you can
			resolve it in the usual ways.
			When using `squash`, and the previous merge with `squash` merged an
			annotated tag of the subtree repository, that tag needs to be
			available locally. If `repository` is given, a missing tag will
			automatically be fetched from that repository.
			Instead of merging the entire history from the subtree project,
			produce only a single commit that contains all the differences you
			want to merge, and then merge that new commit into your project.
			Using this option helps to reduce log clutter. People rarely want
			to see every change that happened between v1.0 and v1.1 of the
			library they’re using, since none of the interim versions were ever
			included in their application.
			Using `squash` also helps avoid problems when the same subproject
			is included multiple times in the same project, or is removed and
			then re_added. In such a case, it doesn’t make sense to combine the
			histories anyway, since it’s unclear which part of the history
			belongs to which subtree.
			Furthermore, with `squash`, you can switch back and forth between
			different versions of a subtree, rather than strictly forward.  git
			subtree merge `squash` always adjusts the subtree to match the
			exactly specified commit, even if getting to that commit would
			require undoing some changes that were added earlier.
			Whether or not you use `squash`, changes made in your local
			repository remain intact and can be later split and send upstream
			to the subproject.

			:param message:
				Specify `message` as the commit message for the merge commit.
		"""
		self.__run(
			"push",
			{
				"annotate": annotate,
				"b": branch,
				"ignore-joins": ignore_joins,
				"onto": onto,
				"rejoin": rejoin,
				"squash": squash,
				"m": message
			},
			repository,
			local_commit,
			remote_ref
		)

	def __run(self, command, options: dict, *args):
		"""Execute the `git-subtree` command."""
		options.update({
			"q": self.quiet,
			"d": self.debug,
			"P": self.prefix
		})
		for key, value in options.items():
			if value:
				short = len(key) > 1
				if short:
					args += (f"--{key}",)
				else:
					args += (f"-{key}",)
				if value is not True:  # meaning it's not a flag

		subprocess.run(
			[self.command, command, *args],
			cwd=self.repository_path,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
					args += (f"{' ' if short else '='}{value}",)  # example: -m <message>, --message=<message>
