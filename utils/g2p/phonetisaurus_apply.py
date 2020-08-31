#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os, logging, subprocess, time, re, sys
from datetime import datetime
from collections import defaultdict
import tempfile

class G2PModelTester () :
    """G2P Model training wrapper class.

    Phonetisaurus G2P modeling training wrapper class.
    This wraps the alignment, joint n-gram training, and ARPA to
    WFST conversion steps into one command.
    """

    def __init__ (self, model, **kwargs) :
        self.model = model
        self.lexicon_file = kwargs.get ("lexicon", None)
        self.nbest = kwargs.get ("nbest", 1)
        self.thresh = kwargs.get ("thresh", 99)
        self.beam = kwargs.get ("beam", 10000)
        self.greedy = kwargs.get ("greedy", False)
        self.accumulate = kwargs.get ("accumulate", False)
        self.pmass = kwargs.get ("pmass", 0.0)
        self.probs = kwargs.get ("probs", False)
        self.verbose = kwargs.get ("verbose", False)
        self.logger = self.setupLogger ()

    def setupLogger (self) :
        """Setup the logger and logging level.

        Setup the logger and logging level.  We only support
        verbose and non-verbose mode.

        Args:
            verbose (bool): Verbose mode, or not.

        Returns:
            Logger: A configured logger instance.
        """

        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig (
            level=level,
            format="\033[94m%(levelname)s:%(name)s:"\
            "%(asctime)s\033[0m:  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        return logging.getLogger ("phonetisaurus-apply")

    def _loadLexicon (self) :
        """Load the lexicon from a file.

        Load the reference lexicon from a file, and store it
        in a defaultdict (list).
        """

        _lexicon = defaultdict (list)
        if not self.lexicon_file :
            return _lexicon

        self.logger.debug ("Loading lexicon from file...")
        with open (self.lexicon_file, "r") as ifp :
            for line in ifp :
                # py2py3 compatbility,
                if sys.version_info[0] < 3:
                    line = line.decode("utf8").strip ()
                else:
                    line = line.strip ()
                word, pron = re.split (r"\t", line, 1)
                _lexicon [word].append (pron)

        return _lexicon

    def checkPhonetisaurusConfig (self) :
        """Run some basic checks before training.

        Run some basic checks regarding the $PATH, environment,
        and provided data before starting training.

        Raises:
            EnvironmentError: raised if binaries are not found.
        """

        self.logger.debug ("Checking command configuration...")
        for program in ["phonetisaurus-g2pfst"] :
            if not self.which (program) :
                raise EnvironmentError("Phonetisaurus command, '{0}', "\
                    "not found in path.".format (program))

        if self.lexicon_file and not os.path.exists (self.lexicon_file) :
            self.logger.error ("Could not find provided lexicon file.")
            sys.exit (1)

        for key,val in sorted (vars (self).items ()) :
            self.logger.debug (u"{0}:  {1}".format (key, val))

        self.lexicon = self._loadLexicon ()

        return

    def which (self, program) :
        """Basic 'which' implementation for python.

        Basic 'which' implementation for python from stackoverflow:
          * https://stackoverflow.com/a/377028/6739158

        Args:
            program (str): The program name to search the $PATH for.

        Returns:
            path/None: The path to the executable, or None.
        """

        def is_exe (fpath) :
            return os.path.isfile (fpath) and os.access (fpath, os.X_OK)

        fpath, fname = os.path.split (program)
        if fpath:
            if is_exe (program):
                return program
        else:
            for path in os.environ["PATH"].split (os.pathsep) :
                path = path.strip ('"')
                exe_file = os.path.join (path, program)
                if is_exe (exe_file):
                    return exe_file

        return None

    def makeG2PCommand (self, word_list) :
        """Build the G2P command.

        Build the G2P command from the provided arguments.

        Returns:
            list: The command in subprocess list format.
        """

        command = [
            u"phonetisaurus-g2pfst",
            u"--model={0}".format (self.model),
            u"--nbest={0}".format (self.nbest),
            u"--beam={0}".format (self.beam),
            u"--thresh={0}".format (self.thresh),
            u"--accumulate={0}".format (str (self.accumulate).lower ()),
            u"--pmass={0}".format (self.pmass),
            u"--nlog_probs={0}".format (str(not self.probs).lower ()),
            u"--wordlist={0}".format (word_list)
        ]

        self.logger.debug (u" ".join (command))

        return command

    def runG2PCommand (self, word_list_file) :
        """Generate and run the actual G2P command.

        Generate and run the actual G2P command.  Each synthesized
        entry will be yielded back on-the-fly via the subprocess
        stdout readline method.

        Args:
            word_list_file (str): The input word list.
        """
        g2p_command = self.makeG2PCommand (word_list_file)

        self.logger.debug ("Applying G2P model...")

        expected_punc = ['_SPACE', '.', '?', '!', ',']
        with open (os.devnull, "w") as devnull :
            proc = subprocess.Popen (
                g2p_command,
                stdout=subprocess.PIPE,
                stderr=devnull if not self.verbose else None
            )

            for line in proc.stdout :
                parts = re.split (r"\t", line.decode ("utf8").strip ())
                if not len (parts) == 3 :
                    if parts[0] in expected_punc:
                        parts = [parts[0], parts[1], parts[0]]
                    else:
                        self.logger.warning (
                            u"No pronunciation for word: '{0}'".format (parts [0])
                        )
                        continue

                yield parts

        return

    def ApplyG2PModel (self, word_list_file) :
        """Apply the G2P model to a word list.

        Apply the G2P model to a word list. If a lexicon is provided, return
        the first pronunciation found for any given input word, otherwise
        return G2P output.

        Args:
            word_list_file (str): The input word list.
        """
        self.checkPhonetisaurusConfig ()

        if not os.path.exists (word_list_file) \
           or not os.path.isfile (word_list_file) :
            raise IOError("Word list file not found.")

        # TODO: Could send only words not in lexicon to g2p, but would need
        # to reconstruct original word order from the two lists of prons.

        # TODO: Some smarter handling of multiple prons, in case lexicon
        # entries are not sensibly ordered. For example, pass word to g2p
        # returning n-best hypotheses and pick the highest-scoring alternative
        # which is also present in the lexicon?

        line = []
        expected_punc = ['.space', '.', '?', '!', ',']

        for word, score, pron in self.runG2PCommand (word_list_file) :
            if word in self.lexicon:
                # take first entry for target word in lexicon, e.g. assuming
                # lexicon entries are sorted by frequency
                line += self.lexicon[word][0].split(' ')
            elif word in expected_punc:
                # just in case some punc is assigned a pron
                line += [word]
            else :
                line += pron.split(' ')

        line = u"|".join(line).replace(".space", " ").strip(" |")
        # return None if empty string for compatibility with TTS.utils.text.text2phone
        return line if line else None

if __name__ == "__main__" :
    import sys, argparse

    example = "{0} --model train/model.fst --word_list word.list".format (sys.argv [0])

    parser  = argparse.ArgumentParser (description=example)
    parser.add_argument ("--model", "-m", help="Phonetisaurus G2P fst model.",
                         required=True)
    parser.add_argument ("--lexicon", "-l", help="Optional reference lexicon.",
                         required=False)
    parser.add_argument ("--nbest", "-n", help="Maximum number of hypotheses "
                         "to produce.  Overridden if --pmass is set.",
                         default=1, type=int)
    parser.add_argument ("--beam", "-b", help="Search 'beam'.",
                         default=10000, type=int)
    parser.add_argument ("--thresh", "-t", help="Pruning threshold for n-best.",
                         default=99.0, type=float)
    parser.add_argument ("--greedy", "-g", help="Use the G2P even if a "
                         "reference lexicon has been provided.", default=False,
                         action="store_true")
    parser.add_argument ("--accumulate", "-a", help="Accumulate probabilities "
                         "across unique pronunciations.", default=False,
                         action="store_true")
    parser.add_argument ("--pmass", "-p", help="Select the maximum number of "
                         "hypotheses summing to P total mass for a word.",
                         default=0.0, type=float)
    parser.add_argument ("--probs", "-pr", help="Print exp(-val) "
                         "instead of default -log values.", default=False,
                         action="store_true")
    parser.add_argument ("--word_list", "-wl", help="Input word or word list to apply "
                        "G2P model to.", type=str)

    parser.add_argument ("--verbose", "-v", help="Verbose mode.",
                         default=False, action="store_true")
    args = parser.parse_args ()

    tester = G2PModelTester (
        args.model,
        **{key:val for key,val in args.__dict__.items ()
           if not key in ["model","word_list"]}
    )

    tester.ApplyG2PModel (args.word_list)
