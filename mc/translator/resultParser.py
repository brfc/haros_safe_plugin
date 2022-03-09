# Generated from result.g4 by ANTLR 4.5.1
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"\13:\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write(u"\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\3\3")
        buf.write(u"\3\5\3\34\n\3\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\5\6")
        buf.write(u"\'\n\6\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\5\t\63")
        buf.write(u"\n\t\3\n\3\n\3\n\3\13\3\13\3\13\2\2\f\2\4\6\b\n\f\16")
        buf.write(u"\20\22\24\2\2\62\2\26\3\2\2\2\4\31\3\2\2\2\6\35\3\2\2")
        buf.write(u"\2\b \3\2\2\2\n&\3\2\2\2\f(\3\2\2\2\16*\3\2\2\2\20\62")
        buf.write(u"\3\2\2\2\22\64\3\2\2\2\24\67\3\2\2\2\26\27\5\4\3\2\27")
        buf.write(u"\30\7\2\2\3\30\3\3\2\2\2\31\33\5\6\4\2\32\34\5\4\3\2")
        buf.write(u"\33\32\3\2\2\2\33\34\3\2\2\2\34\5\3\2\2\2\35\36\5\b\5")
        buf.write(u"\2\36\37\5\n\6\2\37\7\3\2\2\2 !\7\4\2\2!\"\7\5\2\2\"")
        buf.write(u"#\7\6\2\2#\t\3\2\2\2$\'\5\f\7\2%\'\5\16\b\2&$\3\2\2\2")
        buf.write(u"&%\3\2\2\2\'\13\3\2\2\2()\7\7\2\2)\r\3\2\2\2*+\7\b\2")
        buf.write(u"\2+,\7\t\2\2,-\5\20\t\2-\17\3\2\2\2.\63\5\22\n\2/\60")
        buf.write(u"\5\22\n\2\60\61\5\20\t\2\61\63\3\2\2\2\62.\3\2\2\2\62")
        buf.write(u"/\3\2\2\2\63\21\3\2\2\2\64\65\7\n\2\2\65\66\5\24\13\2")
        buf.write(u"\66\23\3\2\2\2\678\7\13\2\28\25\3\2\2\2\5\33&\62")
        return buf.getvalue()


class resultParser ( Parser ):

    grammarFileName = "result.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"<INVALID>", u"'Check '", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"'---INSTANCE---\n'" ]

    symbolicNames = [ u"<INVALID>", u"WHITESPACE", u"TYPE", u"NAME", u"SCOPE", 
                      u"UNSATISFIABLE", u"INSTANCE", u"METAINFO", u"STATENAME", 
                      u"FIELDESCRIPTION" ]

    RULE_gr = 0
    RULE_output = 1
    RULE_command = 2
    RULE_name = 3
    RULE_result = 4
    RULE_unsat = 5
    RULE_sat = 6
    RULE_sts = 7
    RULE_st = 8
    RULE_descriptions = 9

    ruleNames =  [ u"gr", u"output", u"command", u"name", u"result", u"unsat", 
                   u"sat", u"sts", u"st", u"descriptions" ]

    EOF = Token.EOF
    WHITESPACE=1
    TYPE=2
    NAME=3
    SCOPE=4
    UNSATISFIABLE=5
    INSTANCE=6
    METAINFO=7
    STATENAME=8
    FIELDESCRIPTION=9

    def __init__(self, input):
        super(resultParser, self).__init__(input)
        self.checkVersion("4.5.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class GrContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.GrContext, self).__init__(parent, invokingState)
            self.parser = parser

        def output(self):
            return self.getTypedRuleContext(resultParser.OutputContext,0)


        def EOF(self):
            return self.getToken(resultParser.EOF, 0)

        def getRuleIndex(self):
            return resultParser.RULE_gr

        def enterRule(self, listener):
            if hasattr(listener, "enterGr"):
                listener.enterGr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitGr"):
                listener.exitGr(self)




    def gr(self):

        localctx = resultParser.GrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_gr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.output()
            self.state = 21
            self.match(resultParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OutputContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.OutputContext, self).__init__(parent, invokingState)
            self.parser = parser

        def command(self):
            return self.getTypedRuleContext(resultParser.CommandContext,0)


        def output(self):
            return self.getTypedRuleContext(resultParser.OutputContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_output

        def enterRule(self, listener):
            if hasattr(listener, "enterOutput"):
                listener.enterOutput(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitOutput"):
                listener.exitOutput(self)




    def output(self):

        localctx = resultParser.OutputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_output)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.command()
            self.state = 25
            _la = self._input.LA(1)
            if _la==resultParser.TYPE:
                self.state = 24
                self.output()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CommandContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.CommandContext, self).__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(resultParser.NameContext,0)


        def result(self):
            return self.getTypedRuleContext(resultParser.ResultContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_command

        def enterRule(self, listener):
            if hasattr(listener, "enterCommand"):
                listener.enterCommand(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitCommand"):
                listener.exitCommand(self)




    def command(self):

        localctx = resultParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_command)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.name()
            self.state = 28
            self.result()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.NameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def TYPE(self):
            return self.getToken(resultParser.TYPE, 0)

        def NAME(self):
            return self.getToken(resultParser.NAME, 0)

        def SCOPE(self):
            return self.getToken(resultParser.SCOPE, 0)

        def getRuleIndex(self):
            return resultParser.RULE_name

        def enterRule(self, listener):
            if hasattr(listener, "enterName"):
                listener.enterName(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitName"):
                listener.exitName(self)




    def name(self):

        localctx = resultParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(resultParser.TYPE)
            self.state = 31
            self.match(resultParser.NAME)
            self.state = 32
            self.match(resultParser.SCOPE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ResultContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.ResultContext, self).__init__(parent, invokingState)
            self.parser = parser

        def unsat(self):
            return self.getTypedRuleContext(resultParser.UnsatContext,0)


        def sat(self):
            return self.getTypedRuleContext(resultParser.SatContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_result

        def enterRule(self, listener):
            if hasattr(listener, "enterResult"):
                listener.enterResult(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitResult"):
                listener.exitResult(self)




    def result(self):

        localctx = resultParser.ResultContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_result)
        try:
            self.state = 36
            token = self._input.LA(1)
            if token in [resultParser.UNSATISFIABLE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.unsat()

            elif token in [resultParser.INSTANCE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.sat()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class UnsatContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.UnsatContext, self).__init__(parent, invokingState)
            self.parser = parser

        def UNSATISFIABLE(self):
            return self.getToken(resultParser.UNSATISFIABLE, 0)

        def getRuleIndex(self):
            return resultParser.RULE_unsat

        def enterRule(self, listener):
            if hasattr(listener, "enterUnsat"):
                listener.enterUnsat(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitUnsat"):
                listener.exitUnsat(self)




    def unsat(self):

        localctx = resultParser.UnsatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_unsat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(resultParser.UNSATISFIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SatContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.SatContext, self).__init__(parent, invokingState)
            self.parser = parser

        def INSTANCE(self):
            return self.getToken(resultParser.INSTANCE, 0)

        def METAINFO(self):
            return self.getToken(resultParser.METAINFO, 0)

        def sts(self):
            return self.getTypedRuleContext(resultParser.StsContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_sat

        def enterRule(self, listener):
            if hasattr(listener, "enterSat"):
                listener.enterSat(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSat"):
                listener.exitSat(self)




    def sat(self):

        localctx = resultParser.SatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_sat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(resultParser.INSTANCE)
            self.state = 41
            self.match(resultParser.METAINFO)
            self.state = 42
            self.sts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.StsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def st(self):
            return self.getTypedRuleContext(resultParser.StContext,0)


        def sts(self):
            return self.getTypedRuleContext(resultParser.StsContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_sts

        def enterRule(self, listener):
            if hasattr(listener, "enterSts"):
                listener.enterSts(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSts"):
                listener.exitSts(self)




    def sts(self):

        localctx = resultParser.StsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_sts)
        try:
            self.state = 48
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.st()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 45
                self.st()
                self.state = 46
                self.sts()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.StContext, self).__init__(parent, invokingState)
            self.parser = parser

        def STATENAME(self):
            return self.getToken(resultParser.STATENAME, 0)

        def descriptions(self):
            return self.getTypedRuleContext(resultParser.DescriptionsContext,0)


        def getRuleIndex(self):
            return resultParser.RULE_st

        def enterRule(self, listener):
            if hasattr(listener, "enterSt"):
                listener.enterSt(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSt"):
                listener.exitSt(self)




    def st(self):

        localctx = resultParser.StContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_st)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(resultParser.STATENAME)
            self.state = 51
            self.descriptions()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DescriptionsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(resultParser.DescriptionsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def FIELDESCRIPTION(self):
            return self.getToken(resultParser.FIELDESCRIPTION, 0)

        def getRuleIndex(self):
            return resultParser.RULE_descriptions

        def enterRule(self, listener):
            if hasattr(listener, "enterDescriptions"):
                listener.enterDescriptions(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDescriptions"):
                listener.exitDescriptions(self)




    def descriptions(self):

        localctx = resultParser.DescriptionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_descriptions)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(resultParser.FIELDESCRIPTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





